import "https://cdn.jsdelivr.net/npm/molstar@latest/build/viewer/molstar.js";

function render({ model, el }) {
    let viewerContainer = document.createElement("div");
    viewerContainer.id = "viewer_container";

    viewerContainer.style.height = model.get("height");
    viewerContainer.style.width = model.get("width");

    // Make the container responsive
    viewerContainer.style.maxWidth = "100%";
    viewerContainer.style.boxSizing = "border-box";

    el.appendChild(viewerContainer);

    let viewer = null;

    // Initialize the viewer first
    molstar.Viewer.create(viewerContainer, {
        layoutIsExpanded: false,
        layoutShowControls: false
    }).then(v => {
        viewer = v;
        // If we have an initial schema, load it
        updateFromSchema();
    });

    // Function to update the viewer from the schema
    function updateFromSchema() {
        console.log("Updating viewer from schema");
        if (!viewer) return;

        const schema = model.get("schema");
        console.log("Schema:", schema);
        if (schema && schema.trim() !== "") {
            try {
                const mvsData = molstar.PluginExtensions.mvs.MVSData.fromMVSJ(schema);
                molstar.PluginExtensions.mvs.loadMVS(viewer.plugin, mvsData, { sanityChecks: true, replaceExisting: true });
            } catch (error) {
                console.error("Error parsing MolViewSpec schema:", error);
                // Fall back to the default example if schema parsing fails
                const sourceUrl = 'https://raw.githubusercontent.com/molstar/molstar/master/examples/mvs/1h9t_domain_labels.mvsj';
                viewer.loadMvsFromUrl(sourceUrl, 'mvsj');
            }
        } else {
            console.log("Else");
        }
    }

    model.on("change:schema", () => {
        console.log("Schema changed");
        updateFromSchema();
    });

    // Watch for changes to dimensions
    model.on("change:height", () => {
        console.log('change height')
        viewerContainer.style.height = model.get("height");
    });

    model.on("change:width", () => {
        viewerContainer.style.width = model.get("width");
    });
}

export default { render };