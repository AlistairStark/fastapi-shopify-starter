function getParameterByName(name: string, url = window.location.href): string {
  name = name.replace(/[\[\]]/g, "\\$&");
  var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
    results = regex.exec(url);
  if (!results) return "";
  if (!results[2]) return "";
  return decodeURIComponent(results[2].replace(/\+/g, " "));
}

export const config = {
  host: getParameterByName("host"),
  apiKey: "bb7c42ef20cc5a7a25cb4cf345b9cd7b",
};
