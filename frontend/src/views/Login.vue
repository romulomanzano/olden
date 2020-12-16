<template>
  <div class="row justify-content-center">
    <div class="col-lg-5 col-md-7">
      <div class="card bg-secondary shadow border-0">
        <div class="card-body px-lg-6">
          <div
            id="cotter-form-container"
            style="width: 300px; height: 300px;"
          ></div>
        </div>
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
    var cotter = new Cotter("7b2b5c20-0fa9-417e-9a89-284ebe126135"); // 👈 Specify your API KEY ID here
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
