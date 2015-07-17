% include('header.tpl', title=t['title'], keywords=t['kword'])
			<h1><a href=".">{{t['title']}}</a></h1>
			<div id="main">
				<div class="lang_sel">
					<a href="." onClick="javascript:choose_lang({{t['lang']}}); return false;">{{t['lang_sel']}}</a>
				</div>  <!-- land_sel -->
				<div class="info">{{t['main']}}</div>
				<div class="info2"><p>{{t['info']}}</p></div>
				<div id="upload_form">
					<h3>{{t['h3']}}</h3>
					<form name="imgform" method="post" action="/result" enctype="multipart/form-data" onSubmit="javascript:return precheck_file({{t['js_nofile']}}, {{t['js_notype']}}, {{t['uploading']}});">
						<div class="form_file">
							<input type="file" name="imagefile" id="imagefile" />
							<input type="submit" class="submit" id="submitbtn" value="{{t['btn']}}" />
						</div>
					</form>
					<form name="langForm" method="post" action="./">
							<input type="hidden" name="lang" id="lang" value="{{t['lang']}}" />
					</form>
				</div> <!-- upload_form -->
				<div class="ad_banner">
					<script type="text/javascript"><!--
					google_ad_client = "ca-pub-7989610739095174";
					/* 셔터카운터_중간 */
					google_ad_slot = "3474581949";
					google_ad_width = 468;
					google_ad_height = 60;
					googoe_language = "{{t['lang']}}";
					//-->
					</script>
					<script type="text/javascript"
					src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
					</script>
				</div> <!-- ad_banner -->
			</div>	<!-- main -->
			<div id="footer">
				<div id="ft_btns">
					<div>
						<iframe src="//www.facebook.com/plugins/like.php?href=http%3A%2F%2Fnutcrac.kr%2Fsc&amp;send=false&amp;layout=button_count&amp;width=90&amp;show_faces=false&amp;action=like&amp;colorscheme=light&amp;font&amp;height=21" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:90px; height:21px;" allowTransparency="true"></iframe>
					</div>
					<div>
						<g:plusone size="medium"></g:plusone>
						<script type="text/javascript">
						  (function() {
							var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
							po.src = 'https://apis.google.com/js/plusone.js';
							var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
						  })();
						</script>
					</div>
					<div>
						<a href="https://twitter.com/share" class="twitter-share-button">Tweet</a>
						<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="//platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>
					</div>
				</div>	<!-- ft_btns -->
			</div>	<!-- footer -->
% include('footer.tpl')