(function(){

    var noteshandler = {
      props:['get_notes','add_notes','save_notes','delete_notes'],
      data:{},
      methods: {}
   };

   noteshandler.data = function(){
      var data = {
         get_all_notes: this.get_notes,
         add_new_notes: this.add_notes,
         edit_notes: this.save_notes,
         remove_notes:this.delete_notes,
         notes: [],
         color_class: ["red","blue","green","yellow","purple"],
         show_instr: false,
      };
      noteshandler.methods.load.call(data);
      return data;
   };

   noteshandler.methods.load = function(){
      let self = this;
      axios.get(self.get_all_notes)
      .then((res)=>{
         notes=res.data.notes;
         notes.forEach((note) => {
            note.edit = false;
            note.org_content=note.content;
            note.org_title=note.title;
         });
         self.notes=notes;
         reindex(self.notes);
      })
   };

   noteshandler.methods.pick_color= function(index){
      let self = this;
      return "p-"+ self.color_class[index];
   }

   noteshandler.methods.add_note = function(){
      let self = this;
      axios.get(self.add_new_notes)
      .then((res)=>{
         note=res.data.note;
         note.edit= false;
         self.notes.unshift(note);
         reindex(self.notes);
      }).catch((e)=>{
         console.log(e);
      })
   };

   function reindex(notes){
     for (let i =0;i<notes.length;i++) {
          notes[i]._idx = i;
     }
   };

   noteshandler.methods.toggle_edit = function(is_edit,_idx){
         if(is_edit){
            this.notes.forEach((note)=>{note.edit=false;});
         }
         this.notes[_idx].edit=is_edit;
         this.refresh();
   };


   noteshandler.methods.do_save = function(_idx,key,val,edit){
      this.notes.forEach((note)=>{note.edit=false;});
      let self = this;
      axios.post(self.edit_notes,{
         id:self.notes[_idx].id,
         key,
         val
      }).then((res)=>{
         self.notes[_idx]={
            ...res.data.note,
            org_content: res.data.note.content,
            org_title: res.data.note.title,
            edit: edit,
            _idx
         };
         self.refresh();
      })
   };

   noteshandler.methods.do_delete = function(_idx){
      this.notes.forEach((note)=>{note.edit=false;});
      let self = this;
      axios.post(self.remove_notes,{
         id:self.notes[_idx].id,
      }).then(()=>{
         self.notes.splice(_idx,1);
         reindex(self.notes);
      })
   };

   noteshandler.methods.do_cancel = function(_idx){
      let self=this;
      self.notes[_idx].content=self.notes[_idx].org_content;
      self.notes[_idx].title=self.notes[_idx].org_title;
      self.notes[_idx].edit=false;
      self.refresh();
   };

   //code from http://www.endmemo.com/js/pause.php
   noteshandler.methods.wait = function(ms){
       var d = new Date();
       var d2 = null;

       while(d2-d < ms){
         d2 = new Date();
      }
   }

   noteshandler.methods.refresh = function(){
      this.$forceUpdate();
   };

   noteshandler.methods.toggle_instruction = function(){
      this.show_instr=!this.show_instr;
   };

   utils.register_vue_component("noteshandler","components/noteshandler/noteshandler.html",
      function(template){
         noteshandler.template = template.data;
         return noteshandler;
      });

})();
