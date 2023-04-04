export default {
	data() {
		return {
			content: ""
		};
	},
	mounted() {

	},
	methods: {
		send() {
			this.$emit('send', this.content)
		}
	},
	template: `
		<div id="message_entry">
			<input id="message_editor" type="text" v-model="content"></input>
			<div id="message_send" @click="send">
				<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"	 viewBox="0 0 485.725 485.725" xml:space="preserve"><g>	<g>		<path d="M459.835,196.758L73.531,9.826C48.085-2.507,17.46,8.123,5.126,33.569c-6.289,12.975-6.815,28-1.449,41.384			l60.348,150.818h421.7C481.285,213.048,471.972,202.611,459.835,196.758z"/>	</g></g><g>	<g>		<path d="M64.025,259.904L3.677,410.756c-10.472,26.337,2.389,56.177,28.726,66.65c5.963,2.371,12.319,3.603,18.736,3.631			c7.754,0,15.408-1.75,22.391-5.12l386.304-187c12.137-5.854,21.451-16.291,25.89-29.013H64.025z"/>	</g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g></svg>
				<svg xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#"   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"   xmlns:svg="http://www.w3.org/2000/svg"   xmlns="http://www.w3.org/2000/svg"   width="256mm"   height="256mm"   viewBox="0 0 256 256"   version="1.1" >  <defs     id="defs2" />  <metadata     id="metadata5">    <rdf:RDF>      <cc:Work         rdf:about="">        <dc:format>image/svg+xml</dc:format>        <dc:type           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />        <dc:title></dc:title>      </cc:Work>    </rdf:RDF>  </metadata>  <g     id="layer1"     transform="translate(0,-41)">    <path       style="stroke:none;stroke-width:64.20901489;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"       d="M 483.7793 0 A 483.77952 483.77952 0 0 0 0 483.7793 A 483.77952 483.77952 0 0 0 483.7793 967.55859 A 483.77952 483.77952 0 0 0 967.55859 483.7793 L 861.73242 483.7793 A 377.95276 377.95276 0 0 1 483.7793 861.73242 A 377.95276 377.95276 0 0 1 105.82617 483.7793 A 377.95276 377.95276 0 0 1 483.7793 105.82617 L 483.7793 0 z "       transform="matrix(0.26458333,0,0,0.26458333,0,41)"       id="path815" />  </g></svg>
			</div>
		</div>
	`,
};
