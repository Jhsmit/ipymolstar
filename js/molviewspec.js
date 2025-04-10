// import "./widget.css";
import 'molstar/build/viewer/molstar.css';
import { Viewer, PluginExtensions } from 'molstar/build/viewer/molstar'


function updateFromMSVJ(viewer, msvj, options) {
    const mvsData = PluginExtensions.mvs.MVSData.fromMVSJ(msvj);
    PluginExtensions.mvs.loadMVS(viewer.plugin, mvsData, options);
}

function render({ model, el }) {
    const uniqueId = `viewer_container_${Math.random().toString(36).slice(2, 11)}`;
    let viewerContainer = document.createElement("div");
    viewerContainer.id = uniqueId;

    viewerContainer.style.height = model.get("height");
    viewerContainer.style.width = model.get("width");

    // Make the container responsive
    viewerContainer.style.maxWidth = "100%";
    viewerContainer.style.boxSizing = "border-box";

    let viewer = null;

    const ViewerOptions = model.get("viewer_options");

    // Initialize the viewer first
    Viewer.create(viewerContainer, ViewerOptions).then(v => {
        viewer = v;
        // If we have an initial schema, load it
        const msvj = model.get("msvj_data");
        if (msvj && msvj.trim() !== "") {
            const options = model.get('mvs_load_options')
            updateFromMSVJ(viewer, msvj, options)
        };

    });

    el.appendChild(viewerContainer);

    model.on("change:msvj_data", () => {
        console.log("Schema changed");
        const msvj = model.get("msvj_data");
        if (msvj && msvj.trim() !== "") {
            const options = model.get('mvs_load_options')
            updateFromMSVJ(viewer, msvj, options)
        };
    });

    // Watch for changes to dimensions
    model.on("change:height", () => {
        viewerContainer.style.height = model.get("height");
    });

    model.on("change:width", () => {
        viewerContainer.style.width = model.get("width");
    });
}

export default { render };
