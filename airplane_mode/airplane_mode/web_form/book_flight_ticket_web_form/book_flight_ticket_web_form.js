function getRandomArbitrary(min, max) {
  return Math.random() * (max - min) + min;
}

frappe.ready(function() {
	// bind events here
    frappe.web_form.set_value("flight_price", getRandomArbitrary(100, 500));

})
