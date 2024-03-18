import * as myModule from "https://www.ebi.ac.uk/pdbe/pdb-component-library/js/pdbe-molstar-plugin-3.1.3.js";
// import * as myModule from "https://cdn.jsdelivr.net/npm/pdbe-molstar@latest/build/pdbe-molstar-plugin.js"

function standardize_color(str) {
  var ctx = document.createElement("canvas").getContext("2d");
  ctx.fillStyle = str;
  return ctx.fillStyle;
}
function toRgb(color) {
  var hex = standardize_color(color);
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result
    ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16),
      }
    : null;
}

function getHideStructure(model) {
  var hideStructure = [];

  if (model.get("hide_polymer")) {
    hideStructure.push("polymer");
  }
  if (model.get("hide_water")) {
    hideStructure.push("water");
  }
  if (model.get("hide_heteroatoms")) {
    hideStructure.push("het");
  }
  if (model.get("hide_carbs")) {
    hideStructure.push("carbs");
  }
  if (model.get("hide_non_standard")) {
    hideStructure.push("nonStandard");
  }
  if (model.get("hide_coarse")) {
    hideStructure.push("coarse");
  }

  return hideStructure;
}

function getVisibility(model) {
  var visibility = {
    polymer: !model.get("hide_polymer"),
    het: !model.get("hide_heteroatoms"),
    water: !model.get("hide_water"),
    carbs: !model.get("hide_carbs"),
    // maps ?
  };

  return visibility;
}

function getHideCanvasControls(model) {
  var hideCanvasControls = [];
  if (model.get("hide_controls_icon")) {
    hideCanvasControls.push("controlToggle");
  }
  if (model.get("hide_expand_icon")) {
    hideCanvasControls.push("expand");
  }
  if (model.get("hide_settings_icon")) {
    hideCanvasControls.push("controlInfo");
  }
  if (model.get("hide_selection_icon")) {
    hideCanvasControls.push("selection");
  }
  if (model.get("hide_animation_icon")) {
    hideCanvasControls.push("animation");
  }

  return hideCanvasControls;
}

function getOptions(model) {
  var options = {
    moleculeId: model.get("molecule_id"),
    customData: model.get("custom_data"),
    assemblyId: model.get("assembly_id"),
    defaultPreset: model.get("default_preset"),
    ligandView: model.get("ligand_view"),
    alphafoldView: model.get("alphafold_view"),
    superposition: model.get("superposition"),
    superpositionParams: model.get("superposition_params"),
    visualStyle: model.get("visual_style"),
    loadMaps: model.get("load_maps"),
    bgColor: toRgb(model.get("bg_color")),
    highlightColor: toRgb(model.get("highlight_color")),
    selectColor: toRgb(model.get("select_color")),
    lighting: model.get("lighting"),
    validationAnnotation: model.get("validation_annotation"),
    symmetryAnnotation: model.get("symmetry_annotation"),
    pdbeUrl: model.get("pdbe_url"),
    encoding: model.get("encoding"),
    lowPrecisionCoords: model.get("low_precision_coords"),
    selectInteraction: model.get("select_interaction"),
    granularity: model.get("granularity"),
    subscribeEvents: model.get("subscribe_events"),
    hideControls: model.get("hide_controls"),
    hideCanvasControls: getHideCanvasControls(model),
    sequencePanel: model.get("sequence_panel"),
    pdbeLink: model.get("pdbe_link"),
    loadingOverlay: model.get("loading_overlay"),
    expanded: model.get("expanded"),
    landscape: model.get("landscape"),
    reactive: model.get("reactive"),
  };

  return options;
}

function subscribe(model, name, callback) {
  model.on(name, callback);
  return () => model.off(name, callback);
}

function render({ model, el }) {
  let viewerContainer = document.createElement("div");
  viewerContainer.id = "viewer_container";

  viewerContainer.style.height = model.get("height");
  var viewerInstance = new window.PDBeMolstarPlugin();
  viewerInstance.render(viewerContainer, getOptions(model)); //.then(() => {
  el.appendChild(viewerContainer);

  // callbacks to be called after loading is complete
  let callbacksLoadComplete = {
    "change:spin": () => viewerInstance.visual.toggleSpin(model.get("spin")),
    "change:hide_polymer": () => {
      viewerInstance.visual.visibility({ polymer: !model.get("hide_polymer") });
    },
    "change:hide_water": () => {
      viewerInstance.visual.visibility({ water: !model.get("hide_water") });
    },
    "change:hide_heteroatoms": () => {
      viewerInstance.visual.visibility({ het: !model.get("hide_heteroatoms") });
    },
    "change:hide_carbs": () => {
      viewerInstance.visual.visibility({ carbs: !model.get("hide_carbs") });
    },
    "change:hide_non_standard": () => {
      viewerInstance.visual.visibility({
        nonStandard: !model.get("hide_non_standard"),
      });
    },
    "change:hide_coarse": () => {
      viewerInstance.visual.visibility({ coarse: !model.get("hide_coarse") });
    },
    "change:color_data": () => {
      const selectValue = model.get("color_data");
      if (selectValue !== null) {
        viewerInstance.visual.select(selectValue);
      }
    },
  };

  let otherCallbacks = {
    "change:molecule_id": () => {
      viewerInstance.visual.update(getOptions(model), true);
    },
    "change:custom_data": () => {
      viewerInstance.visual.update(getOptions(model), true);
    },
    "change:bg_color": () => {
      viewerInstance.canvas.setBgColor(toRgb(model.get("bg_color")));
    },
    "change:_reset": () => {
      const resetValue = model.get("_reset");
      if (resetValue !== null) {
        viewerInstance.visual.reset(resetValue);
      }
    },
  };

  let combinedCallbacks = Object.assign(
    {},
    callbacksLoadComplete,
    otherCallbacks
  );

  viewerInstance.events.loadComplete.subscribe(() => {
    // trigger callabacks which need to
    Object.values(callbacksLoadComplete).forEach((callback) => callback());
  });

  // subscribe to events and collect unsubscribe funcs
  let unsubscribes = Object.entries(combinedCallbacks).map(([name, callback]) =>
    subscribe(model, name, callback)
  );

  document.addEventListener("PDB.molstar.mouseover", (e) => {
    const eventData = e.eventData;
    model.set("mouseover_event", eventData);
    model.save_changes();
  });

  // TODO return unsubscribe

  // these require re-render
  // model.on("change:visual_style", () => {
  //     viewerInstance.visual.update({visualStyle: model.get('visual_style')});
  //     console.log(model.get('visual_style'));
  // });

  // model.on("change:lighting", () => {
  //     viewerInstance.visual.update({lighting: model.get('lighting')});
  // });

  // model.on("change:color_data", () => {
  //     const selectValue = model.get("color_data");
  //     if (selectValue !== null) {
  //         viewerInstance.visual.select(selectValue);
  //     }
  // });

  // model.on("change:_focus", () => {
  //   const focusValue = model.get("_focus");
  //   if (focusValue !== null) {
  //     viewerInstance.visual.focus(focusValue);
  //   }
  // });
  // model.on("change:_highlight", () => {
  //   const highlightValue = model.get("_highlight");
  //   if (highlightValue !== null) {
  //     viewerInstance.visual.highlight(highlightValue);
  //   }
  // });
  // model.on("change:_clear_highlight", () => {
  //   1;
  //   viewerInstance.visual.clearHighlight();
  // });
  // model.on("change:_clear_selection", () => {
  //   viewerInstance.visual.clearSelection(model.get("_args")["number"]);
  // });
  // model.on("change:_reset", () => {
  //   const resetValue = model.get("_reset");
  //   if (resetValue !== null) {
  //     viewerInstance.visual.reset(resetValue);
  //   }
  // });
  // model.on("change:_update", () => {
  //   const updateValue = model.get("_update");
  //   if (updateValue !== null) {
  //     viewerInstance.visual.update(updateValue);
  //   }
  // });
  //   model.on("change:molecule_id", () => {
  //     viewerInstance.visual.update(getOptions(model), true);
  //   });
  // model.on("change:spin", () => {
  //   viewerInstance.visual.toggleSpin(model.get("spin"));
  // });
  // model.on("change:hide_polymer", () => {
  //   viewerInstance.visual.visibility({ water: !model.get("hide_polymer") });
  // });
  // model.on("change:hide_water", () => {
  //     viewerInstance.visual.visibility({water:!model.get('hide_water')});
  // });
  // model.on("change:hide_heteroatoms", () => {
  //   viewerInstance.visual.visibility({ water: !model.get("hide_heteroatoms") });
  // });
  // model.on("change:hide_carbs", () => {
  //   viewerInstance.visual.visibility({ water: !model.get("hide_carbs") });
  // });
  // model.on("change:hide_non_standard", () => {
  //   viewerInstance.visual.visibility({
  //     water: !model.get("hide_non_standard"),
  //   });
  // });
  // model.on("change:hide_coarse", () => {
  //   viewerInstance.visual.visibility({ water: !model.get("hide_coarse") });
  // });

  // this could be a loop?
  return () => {
    unsubscribes.forEach((unsubscribe) => unsubscribe());
  };
}

export default { render };
