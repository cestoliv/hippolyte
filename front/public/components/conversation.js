import Editor from '/components/editor.js';

export default {
	components: {
		Editor,
	},
	data() {
		return {
			contact: null,
			use_context: true,
			messages: []
		};
	},
	created() {
		setInterval(() => {
			this.refresh_messages_date()
		}, 10000);
	},
	methods: {
		setContact: function (contact) {
			this.contact = contact
			if (contact) this.load()
		},
		async load() {
			this.messages = []

			await fetch(`${this.contact.endpoint}/queries`)
			.then((response) => {
				return response.json()
			}).then((data) => {
				console.log(data)
				//this.add_message(data.answer_html, 'contact', luxon.DateTime.fromISO(data.timestamp).toJSDate())
				for (const message of data) {
					this.add_message(message.query, 'me', luxon.DateTime.fromISO(message.timestamp).toJSDate())
					this.add_message(message.answer_html, 'contact', luxon.DateTime.fromISO(message.timestamp).toJSDate())
				}
			}).catch((err) => {
				console.error(err)
			})
		},
		async sendMessage(message) {
			this.add_message(message, 'me', new Date())

			await fetch(
				this.contact.endpoint,
				{
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({
						query: message,
						use_context: this.use_context,
					}),
				}
			).then((response) => {
				return response.json()
			}).then((data) => {
				this.add_message(data.answer_html, 'contact', luxon.DateTime.fromISO(data.timestamp).toJSDate())
			}).catch((err) => {
				console.error(err)
			})
		},
		add_message(content, sender, date) {
			this.messages.push({
				content: content,
				sender: sender,
				date: date,
				relative_date: null,
				show_date: false,
			})
			this.refresh_messages_date()

			this.$nextTick(() => {
				this.scroll_to_last_message()
			})
		},
		toggle_message_date(message) {
			message.show_date = !message.show_date
		},
		scroll_to_last_message() {
			let messages_count = document.getElementById("messages_list").children.length
			if(messages_count > 0) {
				document.getElementById("messages_list").children[messages_count - 1].scrollIntoView({behavior: 'smooth'})
			}
		},
		refresh_messages_date() {
			for(let message of this.messages) {
				message.relative_date = luxon.DateTime.fromJSDate(message.date).toRelative()
			}
		},
		close() {
			this.$emit('close')
		}
	},
	template: `
		<div id="messages" v-if="contact">
			<div class="messages_infos">
				<div id="return_to_contact" @click="close">
					<!-- return icon -->
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 492 492"><title>Return</title><path d="M464 207l1 1H136l103-104a27 27 0 000-38l-16-16c-5-6-12-8-19-8s-14 2-19 8L8 227a27 27 0 000 38l177 177c5 6 12 8 19 8s14-2 19-8l16-16a27 27 0 000-37L135 284h330c15 0 27-12 27-27v-23c0-15-13-27-28-27z"/></svg>
				</div>
				<p class="contact_pseudo" v-html="contact.name"></p>

				<div class="separator"></div>

				<!-- settings -->
				<label class="switch">
					<input type="checkbox" v-model="use_context">
					<span class="slider round"></span>
				</label>
			</div>

			<div class="separator"></div>

			<ul id="messages_list">
				<li class="message" v-for="(message, index) in messages" :class="message.sender" @click="toggle_message_date(message)">
					<div>
						<div v-html="message.content" @click="toggle_message_date(message)"></div>
					</div>

					<p v-if="!(message.show_date || index == messages.length - 1)">&nbsp;</p>
					<p v-else v-html="message.relative_date" @click="toggle_message_date(message)"></p>
				</li>
			</ul>

			<Editor @send="sendMessage" />

			<div class="messages_loading" v-if="messages_loading">
				<svg class="messages_loading_spinner" xmlns:dc="http://purl.org/dc/elements/1.1/"   xmlns:cc="http://creativecommons.org/ns#"   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"   xmlns:svg="http://www.w3.org/2000/svg"   xmlns="http://www.w3.org/2000/svg"   width="256mm"   height="256mm"   viewBox="0 0 256 256"   version="1.1" >  <defs	 id="defs2" />  <metadata	 id="metadata5">	<rdf:RDF>	  <cc:Work		 rdf:about="">		<dc:format>image/svg+xml</dc:format>		<dc:type		   rdf:resource="http://purl.org/dc/dcmitype/StillImage" />		<dc:title></dc:title>	  </cc:Work>	</rdf:RDF>  </metadata>  <g	 id="layer1"	 transform="translate(0,-41)">	<path	   style="stroke:none;stroke-width:64.20901489;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"	   d="M 483.7793 0 A 483.77952 483.77952 0 0 0 0 483.7793 A 483.77952 483.77952 0 0 0 483.7793 967.55859 A 483.77952 483.77952 0 0 0 967.55859 483.7793 L 861.73242 483.7793 A 377.95276 377.95276 0 0 1 483.7793 861.73242 A 377.95276 377.95276 0 0 1 105.82617 483.7793 A 377.95276 377.95276 0 0 1 483.7793 105.82617 L 483.7793 0 z "	   transform="matrix(0.26458333,0,0,0.26458333,0,41)"	   id="path815" />  </g></svg>
			</div>
		</div>
		<div id="messages_placeholder" v-else>
			<p>Select a discussion to start chatting!</p>
		</div>
	`,
};
