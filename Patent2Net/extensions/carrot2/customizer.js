const head = document.getElementsByTagName("head")[0];
const script = document.createElement("script");
script.type = "text/javascript";
script.src = "http://localhost:5000/Patent2Net/extensions/carrot2/index.js";
script.dataset.domain = "localhost";
head.appendChild(script);

export default app => {
  app.on("clusteringRequested", e => {
    const plausible = window["plausible"];
    if (plausible) {
      plausible("ClusteringRequested", {
        props: {
          source: e.source,
          docs: Math.ceil(e.docs / 50) * 50, // bucket with the resolution of 50
          app: e.app,
          view: e.view
        }
      });
    }
  });
};