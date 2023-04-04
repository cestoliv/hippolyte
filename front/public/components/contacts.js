export default {
	data() {
		return {
			loaded: false,

			contacts: []
		};
	},
	created() {
		this.load();
	},
	methods: {
		async load() {
			this.contacts = []
			this.loaded = false

			await fetch("/api/v1/contacts").then((response) => {
				return response.json()
			}).then((data) => {
				console.log(data)
				this.contacts = data
				this.loaded = true
			}).catch((err) => {
				console.error(err)
				// error.change_content("An unexpected error occurred")
				// error.show()
				this.loaded = false
			})
		},
		set_conversation(contact) {
			console.log(contact)
			this.$emit('setConversation', contact)
		}
	},
	template: `
		<div id="contacts">
			<div id="sodachat_logo">
				<!-- <img src="/imgs/logo_green.svg"> -->
			</div>

			<div id="contacts_list">
				<ul :class="{ showed: loaded }">
					<li class="contact" v-for="contact in contacts" @click="set_conversation(contact)">
						<img v-bind:src="contact.picture" />
						<span contact_pseudo v-html="contact.name"></span>
					</li>
				</ul>

				<svg id="contacts_loading" :class="{ showed: !loaded }" xmlns:dc="http://purl.org/dc/elements/1.1/"   xmlns:cc="http://creativecommons.org/ns#"   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"   xmlns:svg="http://www.w3.org/2000/svg"   xmlns="http://www.w3.org/2000/svg"   width="256mm"   height="256mm"   viewBox="0 0 256 256"   version="1.1" >  <defs     id="defs2" />  <metadata     id="metadata5">    <rdf:RDF>      <cc:Work         rdf:about="">        <dc:format>image/svg+xml</dc:format>        <dc:type           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />        <dc:title></dc:title>      </cc:Work>    </rdf:RDF>  </metadata>  <g     id="layer1"     transform="translate(0,-41)">    <path       style="stroke:none;stroke-width:64.20901489;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"       d="M 483.7793 0 A 483.77952 483.77952 0 0 0 0 483.7793 A 483.77952 483.77952 0 0 0 483.7793 967.55859 A 483.77952 483.77952 0 0 0 967.55859 483.7793 L 861.73242 483.7793 A 377.95276 377.95276 0 0 1 483.7793 861.73242 A 377.95276 377.95276 0 0 1 105.82617 483.7793 A 377.95276 377.95276 0 0 1 483.7793 105.82617 L 483.7793 0 z "       transform="matrix(0.26458333,0,0,0.26458333,0,41)"       id="path815" />  </g></svg>
			</div>
		</div>
	`,
};
