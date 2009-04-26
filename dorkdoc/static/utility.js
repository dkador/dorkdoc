redirect_to_patient = function() {
    var medical_record_number = document.getElementById('id_medical_record_number').value;
    //alert(medical_record_number);
    window.location = "/dorkdoc/patient/" + medical_record_number + "/";
}