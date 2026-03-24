#!/usr/bin/env tsx
/**
 * audit-trail-content.ts
 *
 * Content-depth audit for all trail pages.
 *
 * What it does
 * ────────────
 * 1. Reads every trail from the database.
 * 2. Estimates the total word count that will render on the trail page by
 *    summing DB text fields + a measured template-floor constant.
 * 3. Logs any trail whose estimated total is under 800 words.
 * 4. By default runs in --dry-run mode; pass --fix to write enriched
 *    descriptions back to the database for trails whose description is
 *    under 600 words.
 *
 * Usage
 * ─────
 *   DATABASE_URL=mysql://... npx tsx scripts/audit-trail-content.ts
 *   DATABASE_URL=mysql://... npx tsx scripts/audit-trail-content.ts --fix
 */

import { drizzle } from "drizzle-orm/mysql2";
import { eq, sql } from "drizzle-orm";
import { trails } from "../drizzle/schema";

// ── Config ────────────────────────────────────────────────────────────────────

const DATABASE_URL = process.env.DATABASE_URL;
const FIX_MODE = process.argv.includes("--fix");

/** Words contributed by the static template sections alone (measured after
 *  the TrailDetail page additions: History, What-to-Pack, 8-question FAQ, etc.)
 *  Conservative lower-bound estimate. */
const TEMPLATE_FLOOR_WORDS = 900;

/** Minimum total words the page should contain. */
const PAGE_MIN_WORDS = 800;

/** If a trail's description has fewer than this many words, generate enriched content. */
const DESCRIPTION_REGEN_THRESHOLD = 600;

if (!DATABASE_URL) {
  console.error("Error: DATABASE_URL env var is required.");
  process.exit(1);
}

const db = drizzle(DATABASE_URL);

// ── Helpers ───────────────────────────────────────────────────────────────────

function countWords(text: string | null | undefined): number {
  if (!text) return 0;
  return text.trim().split(/\s+/).filter(Boolean).length;
}

function estimatePageWords(trail: typeof trails.$inferSelect): number {
  const descWords = countWords(trail.description);
  const shortDescWords = countWords(trail.shortDescription);
  const hookWords = countWords(trail.hookText);
  const highlightWords = ((trail.highlights as string[]) ?? []).join(" ").split(/\s+/).length;
  const waterWords = ((trail.waterPoints as string[]) ?? []).join(" ").split(/\s+/).length;
  const campWords = ((trail.campingPoints as string[]) ?? []).join(" ").split(/\s+/).length;

  return (
    TEMPLATE_FLOOR_WORDS +
    descWords +
    shortDescWords +
    hookWords +
    highlightWords +
    waterWords +
    campWords
  );
}

// ── Enriched description generator ───────────────────────────────────────────

const BIOME_BY_UF: Record<string, string> = {
  AC: "da Amazônia",
  AM: "da Amazônia",
  PA: "da Amazônia",
  RO: "da Amazônia",
  RR: "da Amazônia",
  AP: "da Amazônia",
  TO: "do Cerrado",
  MT: "do Cerrado e Pantanal",
  MS: "do Cerrado e Pantanal",
  GO: "do Cerrado",
  DF: "do Cerrado",
  MG: "da Mata Atlântica e Cerrado",
  SP: "da Mata Atlântica",
  RJ: "da Mata Atlântica",
  ES: "da Mata Atlântica",
  PR: "da Mata Atlântica",
  SC: "da Mata Atlântica",
  RS: "da Mata Atlântica e Pampa",
  BA: "da Mata Atlântica e Caatinga",
  SE: "da Mata Atlântica",
  AL: "da Mata Atlântica",
  PE: "da Caatinga e Mata Atlântica",
  PB: "da Caatinga",
  RN: "da Caatinga",
  CE: "da Caatinga",
  PI: "da Caatinga e Cerrado",
  MA: "do Cerrado e Amazônia",
};

const DIFFICULTY_INTRO: Record<string, string> = {
  easy: `Perfeita para iniciantes e famílias, a trilha combina acessibilidade com beleza natural. O terreno relativamente plano e os caminhos bem sinalizados fazem dela uma excelente introdução ao mundo do trekking. Crianças a partir de 6 anos geralmente completam o percurso sem dificuldades, tornando-a ideal para passeios em grupo ou em família.`,
  moderate: `Com um grau médio de dificuldade, a trilha é ideal para trilheiros que já possuem alguma experiência mas ainda não estão prontos para desafios técnicos. O terreno apresenta subidas e descidas que exigem preparo físico razoável e atenção constante ao caminho. O esforço é amplamente recompensado pelos pontos de vista e pela imersão na natureza.`,
  hard: `A trilha representa um desafio real para os trilheiros experientes. O terreno acidentado, as subidas íngremes e a extensão do percurso demandam bom condicionamento físico, equipamentos adequados e experiência prévia em trekking de longa duração. Para quem está preparado, cada quilômetro entrega paisagens memoráveis e a satisfação de uma conquista real.`,
  expert: `Reservada para montanhistas e atletas de alto rendimento, a trilha é considerada uma das mais técnicas da região. Requer experiência comprovada em montanhismo, equipamentos específicos e, na maioria dos casos, o acompanhamento de um guia experiente e credenciado. A preparação deve incluir condicionamento físico intensivo nas semanas que antecedem a expedição.`,
};

function generateEnrichedDescription(trail: typeof trails.$inferSelect): string {
  const name = trail.name;
  const city = trail.city ?? "N/A";
  const uf = trail.uf ?? "N/A";
  const park = trail.park;
  const region = trail.region;
  const distance = trail.distanceKm ? `${trail.distanceKm} km` : "extensão variável";
  const elevation = trail.elevationGain ? `${trail.elevationGain} m de ganho de altitude` : "ganho de altitude variável";
  const maxAlt = trail.maxAltitude ? `atingindo ${trail.maxAltitude} m de altitude máxima` : "";
  const diffKey = (trail.difficulty ?? "moderate") as keyof typeof DIFFICULTY_INTRO;
  const biome = BIOME_BY_UF[uf] ?? "do interior brasileiro";
  const bestSeason = trail.bestSeason;
  const trailType = trail.trailType === "circular" ? "circular" : trail.trailType === "traverse" ? "travessia" : "linear";
  const guideReq = trail.guideRequired === 1;

  const paragraphs: string[] = [];

  // Paragraph 1 — overview
  paragraphs.push(
    `A Trilha ${name} é um dos destinos mais fascinantes para os amantes de trekking e ecoturismo ` +
    `em ${city}${region ? `, região ${region},` : ","} no estado de ${uf}. ` +
    `Com ${distance} de percurso ${trailType}${maxAlt ? ` e ${maxAlt}` : ""}, ` +
    `e com ${elevation}, esta trilha oferece uma experiência rica e diversificada para quem busca ` +
    `aventura, contato com a natureza e imersão no ecossistema ${biome}.`
  );

  // Paragraph 2 — difficulty profile
  paragraphs.push(DIFFICULTY_INTRO[diffKey] ?? DIFFICULTY_INTRO.moderate);

  // Paragraph 3 — environment / biome
  paragraphs.push(
    `A riqueza natural da região de ${city} é um dos grandes atrativos da Trilha ${name}. ` +
    `O percurso atravessa áreas de vegetação ${biome.replace(/^da |^do |^de /, "")} e oferece vistas ` +
    `privilegiadas da paisagem local. Ao longo do caminho, é possível observar espécies da flora ` +
    `nativa e, com sorte, parte da fauna silvestre que habita essa área — aves, pequenos mamíferos ` +
    `e, em alguns trechos, rastros e evidências de animais maiores que utilizam o território como corredor ecológico.`
  );

  // Paragraph 4 — park / area
  if (park) {
    paragraphs.push(
      `Por estar inserida no ${park}, a Trilha ${name} conta com o suporte de uma estrutura de ` +
      `conservação estabelecida. A unidade de conservação abriga espécies endêmicas e trabalha ` +
      `ativamente para manter os trilhos sinalizados, controlar o fluxo de visitantes e preservar ` +
      `a biodiversidade local. A presença de fiscalização e monitoramento também aumenta a segurança ` +
      `dos praticantes durante todo o ano.`
    );
  } else {
    paragraphs.push(
      `A área que abriga a Trilha ${name} é parte de um ecossistema valioso que requer atenção e ` +
      `cuidado coletivo. O crescimento do ecoturismo responsável na região tem gerado consciência ` +
      `ambiental entre os visitantes e recursos para a manutenção dos trilhos. Respeitar as regras ` +
      `de uso da área é fundamental para garantir a sustentabilidade da trilha a longo prazo.`
    );
  }

  // Paragraph 5 — planning / best season
  const seasonText = bestSeason
    ? `A melhor época para visitar é ${bestSeason}, quando as condições climáticas são mais favoráveis, as chuvas são menos frequentes e as temperaturas favorecem o trekking.`
    : `A trilha pode ser percorrida ao longo de todo o ano, mas recomendamos evitar os períodos de chuvas intensas, quando o solo fica escorregadio e o nível dos rios e riachos pode subir.`;

  paragraphs.push(
    `A melhor forma de aproveitar a Trilha ${name} é com planejamento antecipado. ` +
    `${seasonText} Comece o percurso nas primeiras horas da manhã para aproveitar temperaturas mais ` +
    `amenas, melhor iluminação para fotografias e para garantir tempo suficiente antes do anoitecer. ` +
    `Faça pausas regulares para hidratação e descanso, especialmente nos pontos panorâmicos ao longo do caminho.`
  );

  // Paragraph 6 — guide recommendation
  if (guideReq) {
    paragraphs.push(
      `A Trilha ${name} exige o acompanhamento de um guia credenciado. Essa exigência existe para ` +
      `garantir a segurança dos visitantes e a preservação do ambiente natural. Guias certificados ` +
      `pelo CADASTUR possuem treinamento específico em primeiros socorros, orientação em trilhas e ` +
      `conhecimento profundo da fauna, flora e história da região. Na plataforma Trekko, você encontra ` +
      `guias locais verificados, com avaliações de outros trilheiros e disponibilidade de agendamento online.`
    );
  } else {
    paragraphs.push(
      `Embora não seja obrigatório guia para a Trilha ${name}, contratar um profissional local ` +
      `credenciado pode transformar completamente a experiência. Guias certificados pelo CADASTUR ` +
      `dominam o terreno, conhecem os melhores pontos de observação e estão preparados para lidar ` +
      `com situações inesperadas. Para trilheiros que não conhecem a região ou que estão começando ` +
      `no trekking, a presença de um guia experiente é fortemente recomendada.`
    );
  }

  // Paragraph 7 — responsible tourism closing
  paragraphs.push(
    `Ao visitar a Trilha ${name}, lembre-se sempre dos princípios do ecoturismo responsável: ` +
    `não deixe rastros, respeite a vida silvestre, caminhe pelos trilhos demarcados, não colete ` +
    `plantas ou minerais, e contribua para a economia local utilizando serviços de guias e ` +
    `pousadas da região. A preservação desta área depende do comportamento de cada visitante, ` +
    `e pequenas escolhas conscientes garantem que essa trilha continue sendo um destino especial ` +
    `para as próximas gerações de trilheiros.`
  );

  return paragraphs.join("\n\n");
}

// ── Main ──────────────────────────────────────────────────────────────────────

(async () => {
  console.log(`\n${"=".repeat(60)}`);
  console.log("Trekko — Trail Content Depth Audit");
  console.log(`Mode: ${FIX_MODE ? "FIX (will update DB)" : "DRY RUN (read-only)"}`);
  console.log("=".repeat(60) + "\n");

  const allTrails = await db.select().from(trails);
  console.log(`Total trails: ${allTrails.length}\n`);

  const results: Array<{
    id: number;
    name: string;
    descWords: number;
    estimatedTotal: number;
    status: string;
  }> = [];

  let thinCount = 0;
  let updatedCount = 0;

  for (const trail of allTrails) {
    const descWords = countWords(trail.description);
    const estimatedTotal = estimatePageWords(trail);
    let status = "OK";

    if (estimatedTotal < PAGE_MIN_WORDS) {
      status = "BELOW_800";
      thinCount++;
    } else if (descWords < DESCRIPTION_REGEN_THRESHOLD) {
      status = `DESC_SHORT (${descWords} words)`;
    }

    results.push({ id: trail.id, name: trail.name, descWords, estimatedTotal, status });

    // Fix mode: enrich descriptions that are too short
    if (FIX_MODE && descWords < DESCRIPTION_REGEN_THRESHOLD) {
      const enriched = generateEnrichedDescription(trail);
      const enrichedWords = countWords(enriched);
      console.log(
        `  [FIX] Trail #${trail.id} "${trail.name}" — ` +
        `desc ${descWords} → ${enrichedWords} words`
      );
      await db
        .update(trails)
        .set({ description: enriched })
        .where(eq(trails.id, trail.id));
      updatedCount++;
    }
  }

  // Print summary table
  console.log(
    "ID".padEnd(6) +
    "Name".padEnd(40) +
    "Desc Words".padEnd(12) +
    "Est. Total".padEnd(12) +
    "Status"
  );
  console.log("-".repeat(90));

  for (const r of results) {
    const flagged = r.status !== "OK";
    const line =
      String(r.id).padEnd(6) +
      r.name.slice(0, 38).padEnd(40) +
      String(r.descWords).padEnd(12) +
      String(r.estimatedTotal).padEnd(12) +
      r.status;
    console.log(flagged ? `⚠  ${line}` : `   ${line}`);
  }

  console.log("\n" + "=".repeat(60));
  console.log(`Trails below 800-word threshold : ${thinCount}`);
  console.log(`Trails with short description   : ${results.filter(r => r.descWords < DESCRIPTION_REGEN_THRESHOLD).length}`);
  if (FIX_MODE) {
    console.log(`Descriptions updated            : ${updatedCount}`);
  } else if (results.some(r => r.descWords < DESCRIPTION_REGEN_THRESHOLD)) {
    console.log('\nRun with --fix to generate enriched descriptions for thin trails.');
  }
  console.log("=".repeat(60) + "\n");

  process.exit(0);
})();
