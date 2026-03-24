###############################################################################
# Trekko — CloudFront CDN in front of S3 for trail and blog images
#
# Resources:
#   aws_s3_bucket                        — private image bucket
#   aws_cloudfront_origin_access_control — OAC (replaces legacy OAI)
#   aws_cloudfront_function              — WebP content-negotiation at edge
#   aws_cloudfront_distribution          — CDN distribution
#   aws_s3_bucket_policy                 — allows CloudFront OAC to read
#
# Usage:
#   terraform init
#   terraform apply -var="domain=cdn.trekko.com.br" \
#                   -var="acm_certificate_arn=arn:aws:acm:us-east-1:..."
#
# Prerequisites:
#   • ACM certificate for cdn.trekko.com.br must be in us-east-1 (CloudFront req)
#   • Route 53 CNAME cdn.trekko.com.br → CloudFront domain created after apply
###############################################################################

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# CloudFront is a global service; the provider region can be anything.
# The ACM certificate for custom domains MUST be in us-east-1.
provider "aws" {
  region = var.region
}

provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"
}

###############################################################################
# Variables
###############################################################################

variable "region" {
  description = "AWS region for the S3 bucket (closest to SA users: sa-east-1)"
  default     = "sa-east-1"
}

variable "bucket_name" {
  description = "S3 bucket name (must be globally unique)"
  default     = "trekko-images"
}

variable "domain" {
  description = "Custom CDN domain (e.g. cdn.trekko.com.br)"
  default     = "cdn.trekko.com.br"
}

variable "acm_certificate_arn" {
  description = "ARN of ACM certificate for the custom domain (must be in us-east-1)"
  type        = string
}

###############################################################################
# S3 bucket — private, no public access
###############################################################################

resource "aws_s3_bucket" "images" {
  bucket = var.bucket_name

  tags = {
    Project     = "Trekko"
    Environment = "production"
  }
}

# Block ALL public access — CloudFront OAC authenticates internally
resource "aws_s3_bucket_public_access_block" "images" {
  bucket = aws_s3_bucket.images.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_ownership_controls" "images" {
  bucket = aws_s3_bucket.images.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

# CORS so browsers can load images cross-origin (needed for canvas/WebGL)
resource "aws_s3_bucket_cors_configuration" "images" {
  bucket = aws_s3_bucket.images.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "HEAD"]
    allowed_origins = ["https://trekko.com.br", "https://www.trekko.com.br"]
    expose_headers  = ["ETag"]
    max_age_seconds = 86400
  }
}

###############################################################################
# Origin Access Control (OAC) — replaces legacy Origin Access Identity
###############################################################################

resource "aws_cloudfront_origin_access_control" "images" {
  name                              = "trekko-images-oac"
  description                       = "OAC for Trekko image bucket"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

# Bucket policy — grant CloudFront OAC read access to all objects
resource "aws_s3_bucket_policy" "images" {
  bucket = aws_s3_bucket.images.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowCloudFrontOAC"
        Effect = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.images.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = aws_cloudfront_distribution.images.arn
          }
        }
      }
    ]
  })

  # The policy references the distribution ARN, so Terraform must create the
  # distribution first.
  depends_on = [aws_cloudfront_distribution.images]
}

###############################################################################
# CloudFront Function — WebP content negotiation
#
# Runs at viewer-request stage (before cache lookup).
# If the browser advertises "image/webp" in Accept, rewrites .jpg/.jpeg/.png
# URIs to .webp so CloudFront fetches (and caches) the WebP variant from S3.
# A separate cache policy key on the Accept-derived header ensures WebP and
# non-WebP responses are cached independently.
###############################################################################

resource "aws_cloudfront_function" "webp_rewrite" {
  name    = "trekko-webp-rewrite"
  runtime = "cloudfront-js-2.0"
  comment = "Serve WebP to browsers that support it"
  publish = true
  code    = file("${path.module}/cf-function-webp.js")
}

###############################################################################
# Cache policies
###############################################################################

# Images: very long TTL (trail photos rarely change)
resource "aws_cloudfront_cache_policy" "images_long" {
  name        = "trekko-images-long-cache"
  comment     = "30-day cache for trail/blog images"
  default_ttl = 2592000 # 30 days in seconds
  max_ttl     = 31536000 # 1 year
  min_ttl     = 86400    # 1 day minimum

  parameters_in_cache_key_and_forwarded_to_origin {
    cookies_config {
      cookie_behavior = "none"
    }
    headers_config {
      # Include a derived "x-accept-webp" header (set by the CF Function)
      # so WebP and non-WebP responses get separate cache entries.
      header_behavior = "whitelist"
      headers {
        items = ["x-accept-webp"]
      }
    }
    query_strings_config {
      query_string_behavior = "none"
    }
    # Gzip + Brotli for non-binary assets (has no effect on JPEG/WebP but
    # is harmless and correct for any text files stored in the same bucket)
    enable_accept_encoding_brotli = true
    enable_accept_encoding_gzip   = true
  }
}

###############################################################################
# CloudFront distribution
###############################################################################

resource "aws_cloudfront_distribution" "images" {
  comment             = "Trekko image CDN"
  enabled             = true
  is_ipv6_enabled     = true
  price_class         = "PriceClass_200" # North America + Europe + São Paulo edge
  wait_for_deployment = false

  aliases = [var.domain]

  # ── Origin: the private S3 bucket accessed via OAC ──────────────────────
  origin {
    domain_name              = aws_s3_bucket.images.bucket_regional_domain_name
    origin_id                = "s3-trekko-images"
    origin_access_control_id = aws_cloudfront_origin_access_control.images.id
  }

  # ── Default cache behaviour: all image paths ────────────────────────────
  default_cache_behavior {
    target_origin_id       = "s3-trekko-images"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD", "OPTIONS"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true
    cache_policy_id        = aws_cloudfront_cache_policy.images_long.id

    # WebP rewrite runs before the cache lookup
    function_association {
      event_type   = "viewer-request"
      function_arn = aws_cloudfront_function.webp_rewrite.arn
    }

    # Add security + cache headers to every response
    response_headers_policy_id = aws_cloudfront_response_headers_policy.images.id
  }

  # ── HTTPS with custom domain ─────────────────────────────────────────────
  viewer_certificate {
    acm_certificate_arn      = var.acm_certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  # ── Custom error pages: return the S3 404 cleanly ───────────────────────
  custom_error_response {
    error_code            = 403 # S3 returns 403 for missing objects
    response_code         = 404
    response_page_path    = "/404.html"
    error_caching_min_ttl = 60
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  tags = {
    Project     = "Trekko"
    Environment = "production"
  }
}

###############################################################################
# Response headers policy — Cache-Control + security headers
###############################################################################

resource "aws_cloudfront_response_headers_policy" "images" {
  name    = "trekko-images-headers"
  comment = "Cache-Control and security headers for image responses"

  custom_headers_config {
    items {
      header   = "Cache-Control"
      value    = "public, max-age=2592000, immutable"
      override = true
    }
    items {
      header   = "X-Content-Type-Options"
      value    = "nosniff"
      override = true
    }
  }

  cors_config {
    access_control_allow_credentials = false
    access_control_allow_headers {
      items = ["*"]
    }
    access_control_allow_methods {
      items = ["GET", "HEAD"]
    }
    access_control_allow_origins {
      items = ["https://trekko.com.br", "https://www.trekko.com.br"]
    }
    access_control_max_age_sec = 86400
    origin_override            = false
  }
}

###############################################################################
# Outputs
###############################################################################

output "cloudfront_domain" {
  value       = aws_cloudfront_distribution.images.domain_name
  description = "CloudFront distribution domain — set this as CNAME for cdn.trekko.com.br"
}

output "cloudfront_distribution_id" {
  value       = aws_cloudfront_distribution.images.id
  description = "Distribution ID for cache invalidation (aws cloudfront create-invalidation)"
}

output "s3_bucket_name" {
  value       = aws_s3_bucket.images.bucket
  description = "S3 bucket name — use this in CLOUDFRONT_S3_BUCKET env var"
}

output "s3_bucket_regional_domain" {
  value       = aws_s3_bucket.images.bucket_regional_domain_name
  description = "S3 regional domain (origin for CloudFront)"
}
