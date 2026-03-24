/**
 * CloudFront Function: WebP content negotiation
 * Runtime: cloudfront-js-2.0
 * Stage:   viewer-request (before cache lookup)
 *
 * Strategy
 * ─────────
 * 1. Inspect the viewer's Accept header for "image/webp" support.
 * 2. Set a normalised request header "x-accept-webp: 1|0".
 *    The cache policy whitelists this header as a cache key variant so that
 *    WebP and non-WebP responses are cached in separate slots.
 * 3. If WebP is supported AND the URI ends in .jpg / .jpeg / .png, rewrite
 *    the URI to the equivalent .webp path so CloudFront fetches the WebP
 *    object from S3.  The original URI is left unchanged for other formats.
 *
 * Notes
 * ─────
 * • CloudFront Functions have no async/Promise support — keep code sync.
 * • The function only fires for GET/HEAD (CloudFront default behaviour for
 *   image paths), so no method guard is needed.
 * • S3 must contain the .webp variants at the same path with .webp extension.
 */

function handler(event) {
  var request = event.request;
  var headers = request.headers;

  // Determine whether the viewer supports WebP
  var acceptHeader = (headers["accept"] && headers["accept"].value) || "";
  var supportsWebP = acceptHeader.indexOf("image/webp") !== -1;

  // Normalise to a single-value header for the cache key
  headers["x-accept-webp"] = { value: supportsWebP ? "1" : "0" };

  // Rewrite URI: .jpg / .jpeg / .png → .webp (only for WebP-capable browsers)
  if (supportsWebP) {
    var uri = request.uri;
    if (/\.(jpe?g|png)$/i.test(uri)) {
      request.uri = uri.replace(/\.(jpe?g|png)$/i, ".webp");
    }
  }

  return request;
}
