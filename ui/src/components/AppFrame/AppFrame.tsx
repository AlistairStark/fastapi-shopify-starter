import { Frame, Navigation } from "@shopify/polaris";
import { useLocation } from "react-router-dom";

const Nav: React.FC<{ pathname: string }> = ({ pathname }) => (
  <Navigation location={pathname}>
    <Navigation.Section
      items={[
        {
          url: "/",
          label: "Dashboard",
          exactMatch: true,
        },
        {
          url: "/account",
          label: "Account",
        },
      ]}
    />
  </Navigation>
);

export const AppFrame: React.FC = ({ children }) => {
  const location = useLocation();
  return (
    <Frame
      // topBar={topBarMarkup}
      navigation={<Nav pathname={location.pathname} />}
      // showMobileNavigation={mobileNavigationActive}
      // onNavigationDismiss={toggleMobileNavigationActive}
      // skipToContentTarget={skipToContentRef.current}
    >
      {children}
    </Frame>
  );
};
