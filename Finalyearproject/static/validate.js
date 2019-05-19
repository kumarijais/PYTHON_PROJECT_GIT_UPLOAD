function ValidationEvent()
{
	var name=document.getElementById("name").value;
	var email=document.getElementById("email").value;
	var contact=document.getElementById("contact").value;
	var emailReg=/^\w+([\.-]?\w+)*@\w+([\.]?\w+)*(\.\w{2,3})+$/
	if(name!=''&&email!='' && contact!='')
	{
		if(email.match(emailReg))
		{
		if(document.getElementById("male").checked || document.getElementById("female").checked)
		{
			if(contact.length==10)
			{
				alert("All type of validation has been done");
				return true;
			}
			else{
				alert("contact no must be of 10 digits");
				return false;
			}
		}
		else{
			alert("you must select gender");
			return false;
		}
		}
		else{
			alert("Invalid email address...!");
			return false;
		}
	}
	else{
		alert("All fields are reqd");
	}
}