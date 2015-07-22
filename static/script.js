function precheck_file(t_nofile, t_notype, t_uploading) {
	var ifile = document.getElementById('imagefile').value;
	if (ifile == '') { alert(t_nofile); }
	else {
		var exts = /(.jpg|.jpeg|.nef|.dng|.pef|.png|.bmp)$/i;
		if (exts.test(ifile)) {
			document.getElementById('submitbtn').value = t_uploading;
			document.imgform.submit(); return true; }
		else { alert(t_notype); }
	}
	return false;
}

function choose_lang(lang) {
	lang = (lang == 'ko') ? 'en' : 'ko';
	document.getElementById('lang').value = lang;
	document.langForm.submit();
}