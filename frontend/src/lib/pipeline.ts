/**
 * Ordered pipeline_step values from the backend (approximate execution order).
 * Used for progress UI; revision loops may revisit earlier names — parent tracks max rank.
 */
export const STEP_ORDER: string[] = [
  "init",
  "input_intake",
  "input_router",
  "document_parser",
  "document_parser_skipped",
  "skip_document_parser",
  "merge_after_document",
  "vision_analyzer",
  "vision_analyzer_skipped",
  "skip_vision",
  "merge_after_vision",
  "anomaly_detector",
  "anomaly_detector_skipped",
  "skip_anomaly",
  "merge_after_anomaly",
  "tabular_triage",
  "tabular_triage_skipped",
  "skip_tabular",
  "merge_after_tabular",
  "text_normalizer",
  "text_normalizer_skipped",
  "skip_text_normalizer",
  "fusion_node",
  "retriever",
  "planner_outline",
  "draft_writer",
  "rule_checker",
  "reviewer_agent",
  "revision_node",
  "human_approval",
  "human_approval_auto",
  "approval_api_patch",
  "final_export",
];

const RANK = new Map(STEP_ORDER.map((s, i) => [s, i]));

export function stepRank(step: string | undefined): number {
  if (!step) return -1;
  return RANK.get(step) ?? -1;
}

/** User-facing groups for the progress panel (endStep = inclusive checkpoint). */
export const MILESTONES = [
  { id: "intake", label: "Intake & routing", endStep: "merge_after_document" },
  { id: "modalities", label: "Vision, docs & fusion", endStep: "fusion_node" },
  { id: "rag", label: "Retrieval & outline", endStep: "planner_outline" },
  { id: "draft", label: "Draft & review", endStep: "reviewer_agent" },
  { id: "export", label: "Approval & export", endStep: "final_export" },
] as const;
