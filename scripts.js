function valida()
{
    var pass= document.Login.pass
    var user= document.Login.user
    if (pass.value =='' || user.value=='')
    {
        alert("Debe completar todos los campos")

    }
    else
    {
        document.Login.submit()
    }

}

function validaR()
{
    var user= document.Registro.user
    var pass1= document.Registro.pass1
    var pass2= document.Registro.pass2
    var email= document.Registro.email

    if (pass1.value != pass2.value && (pass1.value!="" || pass2.value!=""))
    {
        alert("Las contraseñas deben ser idénticas en ambos campos ")
    }
    else if( !user.checkValidity() || !pass1.checkValidity() || !pass2.checkValidity() || !document.Registro.email.checkValidity() || user.value.length<5 || pass1.value.length<8)
    {
        if (!user.checkValidity())
        {
            if (user.value.length<5)
            {
                alert("El usuario debe ser de mínimo 5 caracteres")
            }
            else
            {
                alert("Es necesario escribir un nickname")
            }
        }
        else if(!pass1.checkValidity())
        {
            
            if (pass1.value.length<8)
            {
                alert("La contraseña debe tener mínimo 8 caracteres")
            }
            else
            {
                alert("Es necesario escribir contraseña")
            }
        }
        else if(!document.Registro.email.checkValidity())
        {
            alert("El correo es requerido")
        }
    }
    else
    {
        document.Registro.submit()
      
    }

}


function verPwd(nombre, act)
{
    var campo=document.getElementById(nombre);
    if (act)
    {campo.type= "text";}
    else
    {campo.type= "password";}
    
}

function limpiar()
{
 document.getElementById('usuario').value=""   
 document.getElementById('password').value=""      
}

function Recuperar()
{
    if (document.getElementById('email').checkValidity())
    {
        document.Forgot.submit();
    }
    else
    {
        alert('Debe escribir un correo válido para continuar con el proceso')
    }
    
}

function ResetP()
{
    if (document.getElementById('pass1').checkValidity() && document.getElementById('pass1').value==document.getElementById('pass2').value)
    {
        document.reset.submit();
    }
    else
    {
        alert('Debe escribir una contraseña válida debe coincidir en los 2 campos')
    }
}

       

    function MaxSize(file)
    {
        limite=5 // en MB
        var FileSize = file.files[0].size / (1024 ** 2);
        if (FileSize > limite) {
            alert('El archivo '+ file.files[0].name +' tiene un peso de ' + FileSize.toFixed(2) + ' MB y excede el límite de ' + limite + ' MB, debe elegir una imagen más liviana.')
            file.value = ''
        } 
        
    }

    function limpiar(file)
    {
            file.value = ''
    }

    function Subir(file)
    {
        if (document.getElementById('tags').checkValidity() && document.getElementById('upload').checkValidity())
        {
            document.subir.submit();
        }
        else
        {
            alert('Debe seleccionar un archivo y mínimo colocar un tag de 5 caracteres')
        }
    }
        
    function checkEnter(e){
        if(e.keyCode == 13){
            if (document.getElementById('Buscar').checkValidity())
            {
                document.fbuscar.submit();
            }
            else
            {
                alert('Para realizar una búsqueda debe escribir mínimo 4 caracteres y máximo 20 caracteres')
            }
        }
     }

     function CargarDatos(pic)
     {
         
        document.getElementById('tagsImg').value = pic.title
        document.getElementById('descriptionImg').value= document.getElementById("hid-"+pic.name).value
        document.getElementById('nameImg').value = pic.name
        if (document.getElementById("public-"+pic.name).value == 1)
        {
        document.getElementById('publicImg').checked = true
       }
       else
       {
        document.getElementById('publicImg').checked = false
       }
     }

     function VistaEliminar(boton)
     {
         document.getElementById("form-name-submit").value= boton.value
         
         if (boton.value=="Eliminar")
         {
                            
            // Se obtiene el modal, se le asigna la vista en bloque y se le asigna la imagen seleccionada
            document.getElementById("myModal").style.display = "block";
            document.getElementById("img01").src = document.getElementById(document.getElementById('nameImg').value).src;
                        
            
         }


    }
    
    function submit_Img(boton)
    {
        document.getElementById("form-name-submit").value= boton.value
        if (boton.value=="Guardar")
            {
                var tags= document.submitImg.tagsImg
                var description= document.submitImg.descriptionImg
                if (tags.value=="" || tags.value.length<5)
                {
                    alert('Debe escribir mínimo un tag de mínimo 5 caracteres y si desea agregar más los puede separar con comas')
                }
                else 
                {
                    if (confirm ('¿Desea actualizar la información de la foto, esta acción no se puede deshacer.?'))
                    {
                        document.submitImg.submit();
                    }
                }
        }
    }

    function ConfirmDel()
    {
        if (confirm ('¿Al eliminar esta foto no será posible revertir la acción, desea continuar con la eliminación?'))
        {
            document.submitImg.submit();
        }
        else
        {
            document.getElementById("myModal").style.display = "none";
        }
    }
    function CerrarVistaModal()
    {
        document.getElementById("myModal").style.display = "none";
    }

    