import { Page, Card, Button } from "@shopify/polaris";

export const HomePage: React.FC = () => {
  return (
    <Page title="Home">
      <Card sectioned>
        <Button onClick={() => alert("Button clicked!")}>Example button</Button>
      </Card>
    </Page>
  );
};
