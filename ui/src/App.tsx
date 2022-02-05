import React from "react";
import "./App.css";
import { config } from "./services";
import enTranslations from "@shopify/polaris/locales/en.json";

import { AppProvider } from "@shopify/polaris";

import "@shopify/polaris/build/esm/styles.css";
import { Footer, Link } from "./components";
import { Provider } from "@shopify/app-bridge-react";
import { Routing } from "./routing";

function App() {
  console.log(config);
  return (
    <Provider config={config}>
      <AppProvider i18n={enTranslations} linkComponent={Link}>
        <Routing />
        <Footer />
      </AppProvider>
    </Provider>
  );
}

export default App;
