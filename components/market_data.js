// Function to fetch production data from the data.gov.in API
async function fetchProductionData() {
    try {
      const apiKey = '579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b';
      // Construct the endpoint URL
      const endpoint = `https://api.data.gov.in/resource/f20d7d45-e3d8-4603-bc79-15a3d0db1f9a?api-key=${apiKey}&format=json&offset=0&limit=10`;
      
      const response = await fetch(endpoint);
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      
      const result = await response.json();
      console.log("Full API response:", result);
      
      // Extract records from the response
      const records = result.records;
      if (!records || records.length === 0) {
        throw new Error("No records found");
      }
      
      // Build HTML table using the records
      let tableHTML = `
        <table class="table table-striped">
          <thead>
            <tr>
              <th>State</th>
              <th>District</th>
              <th>Wheat (Metric Tonnes)</th>
              <th>Maize (Metric Tonnes)</th>
              <th>Rice (Metric Tonnes)</th>
              <th>Barley (Metric Tonnes)</th>
              <th>Ragi (Metric Tonnes)</th>
              <th>Pulses (Metric Tonnes)</th>
              <th>Common Millets (Metric Tonnes)</th>
              <th>Total Food Grains (Metric Tonnes)</th>
              <th>Chillies (Metric Tonnes)</th>
              <th>Ginger (Metric Tonnes)</th>
              <th>Oil Seeds (Metric Tonnes)</th>
            </tr>
          </thead>
          <tbody>
      `;
      
      records.forEach(record => {
        tableHTML += `
          <tr>
            <td>${record.state || ""}</td>
            <td>${record.district || ""}</td>
            <td>${record.wheat_in_metric_tonnes_ || 0}</td>
            <td>${record.maize_in_metric_tonnes_ || 0}</td>
            <td>${record.rice_in_metric_tonnes_ || 0}</td>
            <td>${record.barley_in_metric_tonnes_ || 0}</td>
            <td>${record.ragi_in_metric_tonnes_ || 0}</td>
            <td>${record.pulses_in_metric_tonnes_ || 0}</td>
            <td>${record.common_millets_in_metric_tonnes_ || 0}</td>
            <td>${record.total_food_grains_in_metric_tonnes_ || 0}</td>
            <td>${record.chillies_in_metric_tonnes_ || 0}</td>
            <td>${record.ginger_in_metric_tonnes_ || 0}</td>
            <td>${record.oil_seeds_in_metric_tonnes_ || 0}</td>
          </tr>
        `;
      });
      
      tableHTML += `</tbody></table>`;
      document.getElementById("productionDataContainer").innerHTML = tableHTML;
      
    } catch (error) {
      console.error("Error fetching production data:", error);
      document.getElementById("productionDataContainer").innerHTML = `
        <p class="text-center text-danger">Error fetching production data</p>
      `;
    }
  }
  
  // Attach event listener to the button
  document.getElementById("loadProductionData").addEventListener("click", fetchProductionData);
  