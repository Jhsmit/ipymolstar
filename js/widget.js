import "./widget.css";
// import "https://www.ebi.ac.uk/pdbe/pdb-component-library/css/pdbe-molstar-3.1.3.css";
// import { PDBeMolstarPlugin } from "https://www.ebi.ac.uk/pdbe/pdb-component-library/js/pdbe-molstar-plugin-3.1.2.js";

// import "https://www.ebi.ac.uk/pdbe/pdb-component-library/js/pdbe-molstar-plugin-3.1.2.js"

import * as myModule from "https://www.ebi.ac.uk/pdbe/pdb-component-library/js/pdbe-molstar-plugin-3.1.2.js"

import { Tldraw } from "@tldraw/tldraw";
// import {PDBeMolstarPlugin} from "@pdbe-molstar/app"
// import * as pdbe from 'pdbe-molstar'

// var pbde = require('pdbe-molstar')

// import {PDBeMolstarPlugin } from "https://esm.sh/pdbe-molstar@3.1.2";
// import {PDBeMolstarPlugin } from "pdbe-molstar";
// import { PDBeMolstarPlugin } from "@3dbionotes/pdbe-molstar";
// import { PDBeMolstarPlugin } from "./pdbe-molstar-plugin-3.1.2.js";

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
