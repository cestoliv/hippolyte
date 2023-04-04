import Contacts from '/components/contacts.js';
import Conversation from '/components/conversation.js';

export default {
	components: {
		Contacts,
		Conversation,
	},
	data() {
		return {
			contact: null,
		};
	},
	created() {
		window.addEventListener('popstate', (event) => {
			if (event.state.contact) {
				this.setConversation(event.state.contact)
			} else {
				this.closeConversation()
			}
		})
	},
	methods: {
		setConversation: function (contact) {
			history.pushState({
				"contact": contact.name,
			}, null, `/${contact.name.toLowerCase()}`)

			this.contact = contact
			this.$refs.conversation.setContact(contact)
		},
		closeConversation: function () {
			history.pushState({
				"contact": null,
			}, null, `/`)

			this.contact = null
			this.$refs.conversation.setContact(null)
		}
	},
	template: `
		<Contacts @set-conversation="setConversation" :class="{ 'mobile-shown': !contact }" />
		<Conversation @close="closeConversation" ref="conversation" :class="{ 'mobile-shown': contact }" />
	`,
};
