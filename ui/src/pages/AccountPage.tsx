import { Page, Card, Button } from "@shopify/polaris";
import { useApi } from "../hooks";
import { ApiRoutes } from "../types";

export const AccountPage: React.FC = () => {
  const data = useApi(ApiRoutes.Ping, {
    method: "get",
    params: { q: "HHHIIIII" },
  });
  console.log("data: ", data);
  return (
    <Page title="Account Page">
      <Card sectioned>
        <Button onClick={() => alert("Button clicked!")}>Account</Button>
      </Card>
    </Page>
  );
};
