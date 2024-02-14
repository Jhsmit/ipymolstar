import * as myModule from "https://www.ebi.ac.uk/pdbe/pdb-component-library/js/pdbe-molstar-plugin-3.1.2.js"

function render({ model, el }) {
	let viewerContainer  = document.createElement("div");
	viewerContainer.id = 'viewer_container';
	viewerContainer.style.width = '500px';
	viewerContainer.style.height = '500px';

	let childDiv = document.createElement('div');
	viewerContainer.appendChild(childDiv);

	var viewerInstance = new window.PDBeMolstarPlugin();

	var options = {
		moleculeId: '1qyn'
	};
    
	viewerInstance.render(childDiv, options);

	el.appendChild(viewerContainer);
}

export default { render };
