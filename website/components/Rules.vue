<template>
  <div>
    <v-container>
      <v-row>
        <v-col class="box">
          <v-row class="pa-2"><h3>External Address:</h3></v-row>
          <v-row class="pa-2"
            ><h3>{{ ext_ip }}</h3></v-row
          >
        </v-col>
        <v-col class="box">
          <v-row class="pa-2"><h3>Protocol:</h3></v-row>
          <v-row class="pa-2"
            ><h3>{{ proto }}</h3></v-row
          >
        </v-col>
        <v-col class="box">
          <v-row class="pa-2"><h3>External Port:</h3></v-row>
          <v-row class="pa-2"
            ><h3>{{ eport }}</h3></v-row
          >
        </v-col>
        <v-col class="box">
          <v-row class="pa-2"><h3>Internal Port:</h3></v-row>
          <v-row class="pa-2"
            ><h3>{{ iport }}</h3></v-row
          >
        </v-col>
        <v-col class="col-auto">
          <!-- <v-btn color="#2F9E00" dark><v-icon>mdi-grease-pencil</v-icon></v-btn> -->
          <EditRules
            :curIP="ext_ip"
            :curProto="proto"
            :curEport="eport"
            :curIport="iport"
            @update="updatepage"
          />
        </v-col>
        <v-col class="col-auto">
          <v-btn color="error" dark @click="removeRule"
            ><v-icon>mdi-trash-can-outline</v-icon></v-btn
          >
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import EditRules from '../components/EditRules.vue'
import axios from 'axios'
export default {
  components: {
    EditRules,
  },
  name: 'Rules',
  props: ['ext_ip', 'proto', 'eport', 'iport'],
  data() {
    return {
      url: 'https://api.quix.click/api/v1/client/backends/modify?id=',
      Authorization: this.$auth.$storage.getState('_token.local'),
    }
  },
  methods: {
    async removeRule() {
      const config = {
        headers: {
          'Content-Type': 'application/json',
          Authorization: this.Authorization, //Change this
        },
      }
      var info = {
        cmd: [
          {
            op: 'delete_rule',
            data: {},
          },
        ],
      }
      info.cmd[0].data = {
        ext_ip: this.ext_ip,
        proto: this.proto,
        eport: this.eport,
        iport: this.iport,
      }
      console.log(info)
      try {
        let res = await axios.patch(
          this.url + this.$route.params.id,
          info,
          config
        )
      } catch (error) {
        console.log(error)
      }
      this.$emit("update",true)
    },
    updatepage(){
      this.$emit("update",true)
    }
  },
}
</script>

<style>
.box {
  border: 2px solid #0f4c75;
}
</style>