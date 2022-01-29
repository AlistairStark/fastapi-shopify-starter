import { useState } from "react";
import { axios } from "../services";
import { ApiRoutes } from "../types";
import { isEqual } from "lodash";
import { useAppBridge } from "@shopify/app-bridge-react";
import { getSessionToken } from "@shopify/app-bridge-utils";

type Options = {
  params?: { [key: string]: any };
  body?: any;
  method?: "post" | "get" | "patch" | "delete" | "put";
};

export function useApi<Type>(
  url?: ApiRoutes,
  options: Options = {
    method: "get",
  }
): {
  data: Type | undefined;
  error: string;
  loading: boolean;
  makeRequest: (newUrl?: ApiRoutes, newOpts?: Options) => void;
} {
  const [data, setData] = useState<Type | undefined>(undefined);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [curOptions, setCurOptions] = useState<Options>({});
  const [curUrl, setCurUrl] = useState<ApiRoutes>(ApiRoutes.None);
  const app = useAppBridge();

  const fetch = async (fetchUrl: ApiRoutes, opts: Options) => {
    setLoading(true);
    const method = opts.method ? opts.method : "get";
    try {
      const token = await getSessionToken(app);
      const res = await axios({
        method,
        url: fetchUrl as string,
        data: opts.body,
        params: opts.params,
        headers: {
          authorization: token,
        },
      });
      setData(res.data);
    } catch (err: any) {
      setError(err);
    }
    setLoading(false);
  };
  if (url && (url !== curUrl || !isEqual(options, curOptions))) {
    setCurUrl(url as ApiRoutes);
    setCurOptions(options);
    fetch(url as ApiRoutes, options);
  }
  const makeRequest = (newUrl?: ApiRoutes, newOpts?: Options) => {
    if (newUrl) {
      setCurUrl(newUrl);
    }
    if (newOpts) {
      setCurOptions(newOpts);
    }
    if (!newUrl && !newOpts && curUrl !== ApiRoutes.None) {
      fetch(curUrl, curOptions);
    }
  };
  return { data, error, loading, makeRequest };
}
