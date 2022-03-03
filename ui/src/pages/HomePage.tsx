import { Page, Card, Button } from "@shopify/polaris";
import { useI18n } from "@shopify/react-i18n";

export const HomePage: React.FC = () => {
  const [i18n] = useI18n();
  return (
    <Page title="Home">
      <Card sectioned>
        <Button onClick={() => alert("Button clicked!")}>
          {i18n.translate("Test.Button")}
        </Button>
      </Card>
    </Page>
  );
};
