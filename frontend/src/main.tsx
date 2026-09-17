import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import InteractiveMap from "./features/map/InteractiveMap";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <InteractiveMap />
  </StrictMode>,
);
