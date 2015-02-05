$(document).ready(function(){
	
	var word_list = JSON.parse($('#wordle').text());
	$('#wordle').text("");
	
	var fill = d3.scale.category20();
	  d3.layout.cloud().size([650, 300])
	      .words(word_list.map(function(d) {
	        return {text: d[0], size: d[1] * 50};
	      }))
	      .padding(5)
	      .rotate(0)
	      .font("Arial")
	      .fontSize(function(d) { return d.size; })
	      .on("end", draw)
	      .start();
	      
	  function draw(words) {
	    d3.select("#wordle").append("svg")
	        .attr("width", 650)
	        .attr("height", 300)
	      .append("g")
	        .attr("transform", "translate(150,150)")
	      .selectAll("text")
	        .data(words)
	      .enter().append("text")
	        .style("font-size", function(d) { return d.size + "px"; })
	        .style("font-family", "Arial")
	        .style("fill", function(d, i) { return fill(i); })
	        .attr("text-anchor", "middle")
	        .attr("transform", function(d) {
	          return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
	        })
	        .text(function(d) { return d.text; });
	  }
	 });