import React from "react";
import "./App.css";
import { config } from "./services";
import enTranslations from "@shopify/polaris/locales/en.json";

import { AppProvider } from "@shopify/polaris";

import "@shopify/polaris/build/esm/styles.css";
import { Footer, Link } from "./components";
import { Provider } from "@shopify/app-bridge-react";
import { Routing } from "./routing";
import { I18nContext, I18nManager, useI18n } from "@shopify/react-i18n";

const locale = "en";

const Providers: React.FC = ({ children }) => {
  const [i18n] = useI18n({
    id: "Polaris",
    fallback: enTranslations,
    translations(locale: string) {
      return import(
        /* webpackChunkName: "Polaris-i18n", webpackMode: "lazy-once" */ `@shopify/polaris/locales/${locale}.json`
      ).then((dictionary) => dictionary && dictionary.default);
    },
  });

  return (
    <Provider config={config}>
      <AppProvider i18n={i18n.translations} linkComponent={Link}>
        {children}
      </AppProvider>
    </Provider>
  );
};

const AppContents: React.FC = ({ children }) => {
  const [i18n, ShareTranslations] = useI18n({
    id: "Custom",
    translations(locale: string) {
      return import(
        /* webpackMode: "lazy-once" */ `./translations/${locale}.json`
      ).then((dictionary) => dictionary && dictionary.default);
    },
  });

  return <ShareTranslations>{children}</ShareTranslations>;
};

function App() {
  const i18nManager = new I18nManager({
    locale,
    onError: (error) => console.error(error),
  });

  return (
    <I18nContext.Provider value={i18nManager}>
      <Providers>
        <AppContents>
          <Routing />
          <Footer />
        </AppContents>
      </Providers>
    </I18nContext.Provider>
  );
}

export default App;
