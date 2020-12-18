<template>
  <v-row>
    <v-row>
      <v-card-title class="display-2"> Quix Pricing Model </v-card-title>
    </v-row>
    <v-container class="fill-height" fluid style="min-height: 434px">
      <v-fade-transition mode="out-in">
        <v-row>
          <v-col cols="6">
            <v-card>
              <v-card-text id="header" class="display-1"><strong><i>Basic Pack</i></strong></v-card-text>
              <ul>
                  <li><v-card-text class="headline elements">$1.99 per Month</v-card-text></li>
                  <li><v-card-text class="headline elements">40GB per Month</v-card-text></li>
                  <li><v-card-text class="headline elements">204 Game Hours</v-card-text></li>
                  <li><v-card-text class="headline elements">4,000 Website Visitors</v-card-text></li>
              </ul>
            </v-card>
          </v-col>

          <v-col cols="6">
            <v-card>
              <v-card-text id="header" class="display-1"><strong><i>Overage Fees</i></strong></v-card-text>
              <ul>
                  <li><v-card-text class="headline elements">$0.05</v-card-text></li>
                  <li><v-card-text class="headline elements">1 GB</v-card-text></li>
                  <li><v-card-text class="headline elements">5 Game Hours</v-card-text></li>
                  <li><v-card-text class="headline elements">100 Website Visitors</v-card-text></li>
              </ul>
            </v-card>
          </v-col>
          <v-col cols="6">
            <v-card>
              <v-card-text id="header" class="display-1"><strong><i>Support Pack</i></strong></v-card-text>
              <ul>
                  <li><v-card-text class="headline elements">$50 per Hour</v-card-text></li>
                  <li><v-card-text class="headline elements">Quxi Remote Support</v-card-text></li>
                  <li><v-card-text class="headline elements">No Technical Knowledge Required</v-card-text></li>
                  <li><v-card-text class="headline elements">We will fix your issues from anywhere</v-card-text></li>
              </ul>
            </v-card>
          </v-col>
          <v-col cols="6">
            <v-card>
              <v-card-text id="header" class="display-1"><strong><i>Quix Fast Response</i></strong></v-card-text>
              <ul>
                  <li><v-card-text class="headline elements">$250 per Month</v-card-text></li>
                  <li><v-card-text class="headline elements">10 Hours of Premium remote support</v-card-text></li>
                  <li><v-card-text class="headline elements">4 Hours SLA</v-card-text></li>
                  <li><v-card-text class="headline elements">After $45/hour</v-card-text></li>
              </ul>
            </v-card>
          </v-col>
          <v-col cols="6">
            <v-card>
              <v-card-text id="header" class="display-1"><strong><i>Quix Business Pack</i></strong></v-card-text>
              <ul>
                  <li><v-card-text class="headline elements">$3000 per Year</v-card-text></li>
                  <li><v-card-text class="headline elements">150 hours of remote support</v-card-text></li>
                  <li><v-card-text class="headline elements">2 hours SLA</v-card-text></li>
                  <li><v-card-text class="headline elements">After $40/hour</v-card-text></li>
              </ul>
            </v-card>
          </v-col>
        </v-row>
      </v-fade-transition>
    </v-container>
  </v-row>
</template>

<script>
export default {}
</script>

<style>
.title {
  font-size: 55px;
}
.elements{
    color: #ffffff;
}
#header{
    color: #bbe1fa;
}
</style>