<template>
  <div class="row justify-content-center">
    <div class="" style="">
      <div class="card bg-secondary shadow border-0">
        <div id="cotter-form-container" style="height: 350px;"></div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "../axios-auth";
import Cotter from "cotter";

export default {
  name: "login",
  data: () => ({}),
  methods: {},
  mounted() {
    // 1) Make a Config for adding Styles
    var config = {
      ApiKeyID: "464cc449-96da-497a-ab79-07c6452fbc48",
      Styles: {
        input_label: {
          fontFamily: "Roboto",
          fontSize: 16,
          width: 200,
          color: "#626262",
          fontWeight: 600,
        },
        input_text_container_default: {
          backgroundColor: "#e9ecef",
          padding: "5px 5px",
          width: 200,
          borderRadius: 5,
        },
        input_text: {
          backgroundColor: "#e9ecef",
          fontFamily: "Roboto",
          fontSize: 14,
        },
        button_container: {
          borderRadius: 5,
          width: 200,
          height: 30,
          fontWeight: 600,
          fontSize: 14,
          backgroundColor: "#8965e0",
        },
      },

      // your other config...
    };

    var cotter = new Cotter(config); // 👈 Specify your API KEY ID here
    cotter
      .signInWithLink() // to send a verification code, use .signInWithOTP()
      .showEmailForm() // to send via phone number use .showPhoneForm()
      .then((payload) => {
        //Login to backend
        axios
          .post("auth/login", payload)
          .then((res) => {
            this.$store.dispatch("login", res.data);
          })
          .catch((err) => this.$message.error(err.response.data.message));
      });
  },
};
</script>
<style></style>
