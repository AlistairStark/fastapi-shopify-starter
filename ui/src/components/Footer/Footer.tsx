import { FooterHelp } from "@shopify/polaris";
import { Link as ShopifyLink } from "@shopify/polaris";

export const Footer: React.FC = () => (
  <FooterHelp>
    Learn more about{" "}
    <ShopifyLink
      external
      url="https://help.shopify.com/manual/orders/fulfill-orders"
    >
      fulfilling orders
    </ShopifyLink>
  </FooterHelp>
);
