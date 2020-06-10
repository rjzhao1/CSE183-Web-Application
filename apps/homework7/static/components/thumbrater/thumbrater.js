(function(){

    var thumbrater = {
      props:['url','callback_url'],
      data:{},
      methods: {}
   };

   thumbrater.data = function(){
      var data = {
         rating: 0,
         get_url: this.url,
         set_url: this.callback_url
      };
      thumbrater.methods.load.call(data);
      return data;
   };

   thumbrater.methods.set_rating = function(rating){
      let self = this;
      let current_rating = self.rating;
      if(rating===current_rating){
         rating = 0;
      }
      axios
         .get(self.set_url,{
            params: {
               rating:rating,
            }
         }).then(()=>{
            self.rating = rating
         })
   };

   thumbrater.methods.load = function(){
      let self = this;
      axios.get(self.get_url)
      .then((res)=>{
         self.rating = res.data.rating;
      })
   };

   utils.register_vue_component("thumbrater","components/thumbrater/thumbrater.html",
      function(template){
         thumbrater.template = template.data;
         return thumbrater;
      });

})();
