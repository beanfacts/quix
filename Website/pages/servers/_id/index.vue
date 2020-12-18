<template>
  <v-container>
    <v-row class="">
      <b style="font-size: 1.5rem">Server Configuration</b>
    </v-row>
    <v-row class="box ma-2">
      <pre
        class="config pa-2"
      ><b>Servername:</b>      <p>{{serverConfiguration.name}}</p></pre>
      <TextDialog
        class="ma-2 alignright"
        :field="'Change Servername'"
        :jsKey="'name'"
        @item-changed="updateContent"
      />
    </v-row>
    <v-row class="box ma-2">
      <pre
        class="config pa-2"
      ><b>Uplink:</b>          <p>{{serverConfiguration.uplink}}</p></pre>
      <TextDialog
        class="ma-2 alignright"
        :field="'Change Uplink'"
        :jsKey="'uplink'"
        @item-changed="updateContent"
      />
    </v-row>
    <v-row class="box ma-2">
      <pre
        class="config pa-2"
      ><b>Status:</b>          <p>{{serverConfiguration.status}}</p></pre>
    </v-row>
    <v-row class="box ma-2">
      <pre
        class="config pa-2"
      ><b>Location:</b>        <p>{{serverConfiguration.location}}</p></pre>
      <TextDialog
        class="ma-2 alignright"
        :field="'Change Location'"
        :jsKey="'location'"
        @item-changed="updateContent"
      />
    </v-row>
    <v-row>
      <b style="font-size: 1.5rem">Forwarding Rules</b>
      <AddRulesDialog :ExtIP="serverConfiguration.rules" @update="updateContent"/>
    </v-row>
    <Rules
      v-for="(index, i) in serverConfiguration.rules"
      :key="i"
      :ext_ip="index.ext_ip"
      :proto="index.proto"
      :eport="index.eport"
      :iport="index.iport"
      class="ma-2"
      @update="updateContent"
    />
    <VNC v-if="serverConfiguration.name == 'Bobs Server'"/>
  </v-container>
</template>

<script>
import axios from 'axios'
import Rules from '../../../components/Rules.vue'
import TextDialog from '../../../components/TextDialog.vue'
import AddRulesDialog from '../../../components/AddRulesDialog.vue'
import VNC from "../../../components/VNC.vue"

export default {
  components: {
    TextDialog,
    Rules,
    AddRulesDialog,
    VNC
  },
  data() {
    return {
      serverConfiguration: {},
      url:'https://api.quix.click/api/v1/client/backends?id=',
      state: null,
      Authorization: this.$auth.$storage.getState('_token.local'),
      urlModify:'https://api.quix.click/api/v1/client/backends/modify?id='
    }
  },
  async created() {
    const config = {
      headers: {
        Authorization: `${this.Authorization}`,
      },
    }
    try {
      const res = await axios.get(this.url + this.$route.params.id, config)
      this.serverConfiguration = res.data
      console.log("RETURN FROM INDEX",this.serverConfiguration)
    } catch (error) {
      console.log(error)
    }
  },
  methods: {
    updateContent() {
      setTimeout(this.updateConfig, 200)
      console.log("Update Content Function")
    },
    async updateConfig(item, newItem) {
      const config = {
        headers: {
          'Content-Type': 'application/json',
          Authorization: this.Authorization,
        },
      }
      try {
        const res = await axios.get(this.url + this.$route.params.id, config)
        this.serverConfiguration = res.data
        this.$forceUpdate()
        console.log("Update Page")
      } catch (error) {
        console.log(error)
      }
    },
  },
}
</script>

<style>
.config {
  font-size: 1.3rem;
}
.box {
  border: 2px solid #0f4c75;
}
</style>