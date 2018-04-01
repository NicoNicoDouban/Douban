KindEditor.ready(function(K) {  
        K.create('textarea[name=text]',{    
            width:800,  
            height:300,  
            uploadJson: '/admin/upload/kindeditor'  
        });  
});