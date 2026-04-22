import { redirect } from "next/navigation";

/** Legacy route — progress UI lives at `/progress`. */
export default function PipelineRedirectPage() {
  redirect("/progress");
}
