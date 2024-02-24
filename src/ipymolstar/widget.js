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
        

function render({ model, el }) {
	let viewerContainer  = document.createElement("div");
	viewerContainer.id = 'viewer_container';
	viewerContainer.style.width = '100%';
	viewerContainer.style.height = '500px';

	let childDiv = document.createElement('div');
	viewerContainer.appendChild(childDiv);

	var viewerInstance = new window.PDBeMolstarPlugin();

	var options = {
		moleculeId: model.get('molecule_id'),
        customData: model.get('custom_data'),
        bgColor: toRgb(model.get('bg_color')),
        hideStructure: getHideStructure(model),
	};
    
	viewerInstance.render(childDiv, options);
	el.appendChild(viewerContainer);


    model.on("change:_select", () => {
        viewerInstance.visual.select(model.get("_select"));
    });
    
    model.on("change:spin", () => {
        viewerInstance.visual.toggleSpin(model.get('spin'));
    });

    model.on("change:hide_water", () => {
        viewerInstance.visual.visibility({water:!model.get('hide_water')})
    });
    // .. add other structural properties ...

    // cleanup (needed or no?)
    return () => {
        model.off("change:spin");
        model.off("change:hide_water");
    }
    
}

export default { render };
