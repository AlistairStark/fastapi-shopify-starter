import { Page, Card, Button } from "@shopify/polaris";

export const AccountPage: React.FC = () => {
  return (
    <Page title="Account Page">
      <Card sectioned>
        <Button onClick={() => alert("Button clicked!")}>Account</Button>
      </Card>
    </Page>
  );
};
