import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import config from 'devextreme/core/config';
import { licenseKey } from './devextreme-license';
import "./index.css";
import "devextreme/dist/css/dx.material.blue.dark.css";

config({ licenseKey });

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
