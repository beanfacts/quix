<template>
  <v-row justify="center" align="center" dark>
    <v-col cols="12">
      <div class="text-center"></div>
      <v-card>
        <v-card-title class="headline"> Welcome to Quix </v-card-title>
        <v-card-text>
          <p style="font-size: 18px">
            The <i>One Click</i> for server Configuration
          </p>
        </v-card-text>
        <v-card-title class="headline"
          ><strong>Server Complexities </strong></v-card-title
        >
      </v-card>
      <v-container class="fill-height" fluid style="min-height: 434px">
        <v-fade-transition mode="out-in">
          <v-row>
            <v-col cols="6">
              <v-card>
                <v-img
                  src="/pic1.jpg"
                  height="250"
                  class="grey darken-4"
                ></v-img>
                <v-card-title class="title labelpic">
                  Maintain High availability
                </v-card-title>
              </v-card>
            </v-col>

            <v-col cols="6">
              <v-card>
                <v-img
                  src="/pic2.jpg"
                  height="250"
                  class="grey darken-4"
                ></v-img>
                <v-card-title class="title labelpic">
                  Billing Complexity
                </v-card-title>
              </v-card>
            </v-col>
            <v-col cols="6">
              <v-card>
                <v-img
                  src="/pic3.jpg"
                  max-height="250"
                  class="grey darken-4"
                ></v-img>
                <v-card-title class="title labelpic">
                  Server Configuration
                </v-card-title>
              </v-card>
            </v-col>
            <v-col cols="6">
              <v-card>
                <v-img
                  src="/pic4.jpg"
                  max-height="250"
                  class="grey darken-4"
                ></v-img>
                <v-card-title class="title labelpic"> Routing </v-card-title>
              </v-card>
            </v-col>
            <v-col cols="6">
              <v-card>
                <v-img
                  src="/pic5.jpg"
                  max-height="250"
                  class="grey darken-4"
                ></v-img>
                <v-card-title class="title labelpic">
                  Sercurity and Encryption
                </v-card-title>
              </v-card>
            </v-col>
            <v-col cols="6">
              <v-card>
                <v-img
                  src="/pic6.jpg"
                  max-height="250"
                  class="grey darken-4"
                ></v-img>
                <v-card-title class="title labelpic">
                  Port-Forwarding
                </v-card-title>
              </v-card>
            </v-col>
          </v-row>
        </v-fade-transition>
      </v-container>
    </v-col>
  </v-row>
</template>

<script>
export default {
  components: {},
  head() {
    title: 'Quix'
  },
  data() {
    return {
      backgroundUrl: '/BG.jpg',
    }
  },
}
</script>

<style>
.p {
  font-size: 18px;
}
.labelpic {
  background-color: #0f4c75;
}
* {
   color:  #bbe1fa;
}

</style>