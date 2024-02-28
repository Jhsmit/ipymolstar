import * as myModule from "https://www.ebi.ac.uk/pdbe/pdb-component-library/js/pdbe-molstar-plugin-3.1.2.js"


function standardize_color(str){
	var ctx = document.createElement("canvas").getContext("2d");
	ctx.fillStyle = str;
	return ctx.fillStyle;
}
function toRgb(color) {
  var hex = standardize_color(color)
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
	r: parseInt(result[1], 16),
	g: parseInt(result[2], 16),
	b: parseInt(result[3], 16)
  } : null;
}


function getHideStructure(model){
    var hideStructure = [];

    if (model.get('hide_polymer')){
        hideStructure.push("polymer")
    }
    if (model.get('hide_water')){
        hideStructure.push("water")
    }
    if (model.get('hide_heteroatoms')){
        hideStructure.push("het")
    }
    if (model.get('hide_carbs')){
        hideStructure.push("carbs")
    }
    if (model.get('hide_non_standard')){
        hideStructure.push("nonStandard")
    }
    if (model.get('hide_coarse')){
        hideStructure.push("coarse")
    }

    return hideStructure
}

function getHideCanvasControls(model){
    var hideCanvasControls = [];
    if (model.get('hide_controls_icon')) {
        hideCanvasControls.push("controlToggle");
    }
    if (model.get('hide_expand_icon')) {
        hideCanvasControls.push("expand");
    }
    if (model.get('hide_settings_icon')) {
        hideCanvasControls.push("controlInfo");
    }
    if (model.get('hide_selection_icon')) {
        hideCanvasControls.push('selection');
    }
    if (model.get('hide_animation_icon')) {
        hideCanvasControls.push("animation");
    }

    return hideCanvasControls
}

function getOptions(model){
    var options = {
		moleculeId: model.get('molecule_id'),
        customData: model.get('custom_data'),
        assemblyId: model.get('assembly_id'),
        defaultPreset: model.get('default_preset'),
        ligandView: model.get('ligand_view'),
        alphafoldView: model.get('alphafold_view'),
        superposition: model.get('superposition'),
        superpositionParams: model.get('superposition_params'),
        visualStyle: model.get('visual_style'),
        loadMaps: model.get('load_maps'),
        bgColor: toRgb(model.get('bg_color')),
        hideStructure: getHideStructure(model),
        highlightColor: toRgb(model.get('highlight_color')),
        selectColor: toRgb(model.get('select_color')),
        lighting: model.get('lighting'),
        validationAnnotation: model.get('validation_annotation'),
        symmetryAnnotation: model.get('symmetry_annotation'),
        pdbeUrl: model.get('pdbe_url'),
        encoding: model.get('encoding'),
        lowPrecisionCoords: model.get('low_precision_coords'),
        selectInteraction: model.get('select_interaction'),
        granularity: model.get('granularity'),
        subscribeEvents: model.get('subscribe_events'),
        hideControls: model.get('hide_controls'),
        hideCanvasControls: getHideCanvasControls(model),
        sequencePanel: model.get('sequence_panel'),
        pdbeLink: model.get('pdbe_link'),
        loadingOverlay: model.get('loading_overlay'),
        expanded: model.get('expanded'),
        landscape: model.get('landscape'),
        reactive: model.get('reactive')

	};

    return options
}

function render({ model, el }) {
	let viewerContainer  = document.createElement("div");
	viewerContainer.id = 'viewer_container';

    // width is ignored
    // probably some other css setting somewhere which takes priority?
	// viewerContainer.style.width = model.get('width');
	viewerContainer.style.height = model.get('height');

	var viewerInstance = new window.PDBeMolstarPlugin();   
	viewerInstance.render(viewerContainer, getOptions(model));
	el.appendChild(viewerContainer);

    // these require re-render
    // model.on("change:visual_style", () => {
    //     viewerInstance.visual.update({visualStyle: model.get('visual_style')});
    //     console.log(model.get('visual_style'));
    // });

    // model.on("change:lighting", () => {
    //     viewerInstance.visual.update({lighting: model.get('lighting')});
    // });

    model.on("change:_select", () => {
        const selectValue = model.get("_select");
        if (selectValue !== null) {
            viewerInstance.visual.select(selectValue);
        }
    });   
    model.on("change:_focus", () => {
        const focusValue = model.get("_focus");
        if (focusValue !== null) {
            viewerInstance.visual.focus(focusValue);
        }
    });
    model.on("change:_highlight", () => {
        const highlightValue = model.get("_highlight");
        if (highlightValue !== null) {
            viewerInstance.visual.highlight(highlightValue);
        }
    });
    model.on("change:_clear_highlight", () => {
        viewerInstance.visual.clearHighlight();
    });
    model.on("change:_clear_selection", () => {
        viewerInstance.visual.clearSelection(model.get('_args')['number']);
    })
    model.on("change:_set_color", () => {
        const colorValue = model.get("_set_color");
        if (colorValue !== null) {
            viewerInstance.visual.setColor(colorValue);
        }
    });
    model.on("change:_reset", () => {
        const resetValue = model.get("_reset");
        if (resetValue !== null) {
            viewerInstance.visual.reset(resetValue);
        }
    });
    model.on("change:_update", () => {
        const updateValue = model.get("_update");
        if (updateValue !== null) {
            viewerInstance.visual.update(updateValue);
        }
    });
    model.on("change:molecule_id", () => {
        viewerInstance.visual.update(getOptions(model), true);
    });
    model.on("change:spin", () => {
        viewerInstance.visual.toggleSpin(model.get('spin'));
    });
    model.on("change:hide_polymer", () => {
        viewerInstance.visual.visibility({water:!model.get('hide_polymer')});
    });
    model.on("change:hide_water", () => {
        viewerInstance.visual.visibility({water:!model.get('hide_water')});
    });
    model.on("change:hide_heteroatoms", () => {
        viewerInstance.visual.visibility({water:!model.get('hide_heteroatoms')});
    });
    model.on("change:hide_carbs", () => {
        viewerInstance.visual.visibility({water:!model.get('hide_carbs')});
    });
    model.on("change:hide_non_standard", () => {
        viewerInstance.visual.visibility({water:!model.get('hide_non_standard')});
    });
    model.on("change:hide_coarse", () => {
        viewerInstance.visual.visibility({water:!model.get('hide_coarse')});
    });

    // this could be a loop?
    return () => {
        model.off("change:_select");
        model.off("change:_focus");
        model.off("change:_highlight");
        model.off("change:_clear_highlight");
        model.off("change:_clear_selection");
        model.off("change:_set_color");
        model.off("change:_reset");
        model.off("change:_update");
        model.off("change:molecule_id");
        model.off("change:spin");
        model.off("change:hide_polymer");
        model.off("change:hide_water");
        model.off("change:hide_heteroatoms");
        model.off("change:hide_carbs");
        model.off("change:hide_non_standard");
        model.off("change:hide_coarse");
    }
    
}

export default { render };
