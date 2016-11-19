function js_back() {
    history.go( - 1)
}
function pay_sdk_json(data) {
    var json = '{"pay_sdk_type":"' + data['pay_sdk_type'] + '","config":{';
    for (var k in data['config']) {
        json += '"' + k + '":"' + data['config'][k] + '",'
    }
    json = json.substring(0, json.length - 1);
    json += '}}';
    return json
}
function js_pay_sdk(state) {
    if (state == 1) {
        $.showErr("支付成功",
        function() {
            location.reload()
        })
    } else if (state == 2) {} else if (state == 6) {
        $.showErr("支付接口异常",
        function() {
            location.reload()
        })
    } else {
        location.reload()
    }
}
var infinite_loading = false;
function init_scroll_bottom() {
    $(".scroll_bottom_page").hide();
    if ($(".scroll_bottom_page").length > 0) {
        $(".scroll_bottom_page").after("<div class='page-load'></div>");
        $(".page-load").html("努力加载中...~")
    }
    $(window).scroll(function() {
        var totalheight = parseFloat($(window).height()) + parseFloat($(window).scrollTop()) + 100;
        if ($(document).height() <= totalheight) {
            if (infinite_loading) return;
            var next_dom = $(".scroll_bottom_page").find("span.current").next();
            if (next_dom.length > 0) {
                var url = $(".scroll_bottom_page").find("span.current").next().attr("href");
                $(".page-load").html("努力加载中...~");
                infinite_loading = true;
                $.ajax({
                    url: url,
                    type: "POST",
                    success: function(html) {
                        $(".scroll_bottom_list").append($(html).find(".scroll_bottom_list").html());
                        $(".scroll_bottom_page").html($(html).find(".scroll_bottom_page").html());
                        infinite_loading = false;
                        $(".page-load").html("")
                    },
                    error: function() {}
                })
            } else {
                $(".page-load").html("已经到底部了...~")
            }
        }
    })
}
$(document).ready(function() {
    init_ui_button();
    init_ui_textbox();
    init_ui_select();
    init_ui_lazy();
    init_ui_starbar();
    init_ui_confirm();
    init_scroll_bottom();
    if (typeof(appId) != 'undefined') {
        wx.config({
            debug: false,
            appId: appId,
            timestamp: timestamp,
            nonceStr: nonceStr,
            signature: signature,
            jsApiList: ['onMenuShareAppMessage', 'onMenuShareTimeline', 'onMenuShareQQ', 'onMenuShareWeibo', 'onMenuShareQZone', ]
        });
        wx.ready(function() {
            wx.onMenuShareAppMessage({
                title: page_title,
                desc: shar_url,
                link: shar_url,
                imgUrl: imgUrl,
                success: function() {},
                cancel: function() {}
            });
            wx.onMenuShareTimeline({
                title: page_title,
                desc: shar_url,
                link: shar_url,
                imgUrl: imgUrl,
                success: function() {},
                cancel: function() {}
            });
            wx.onMenuShareQQ({
                title: page_title,
                desc: shar_url,
                link: shar_url,
                imgUrl: imgUrl,
                success: function() {},
                cancel: function() {}
            });
            wx.onMenuShareWeibo({
                title: page_title,
                desc: shar_url,
                link: shar_url,
                imgUrl: imgUrl,
                success: function() {},
                cancel: function() {}
            });
            wx.onMenuShareQZone({
                title: page_title,
                desc: shar_url,
                link: shar_url,
                imgUrl: imgUrl,
                success: function() {},
                cancel: function() {}
            })
        })
    }
    gotoTop(500);
    $(".h_search").click(function() {
        $(".pull_down").toggle();
        $(".biz_pull_down").toggle()
    });
    $(".Client").find(".close_but").bind("click",
    function() {
        $(".Client").hide();
        var query = new Object();
        query.act = "close_appdown";
        $.ajax({
            url: AJAX_URL,
            data: query,
            type: "POST",
            success: function() {},
            error: function(o) {}
        })
    });
    try {
        App.apns()
    } catch(ex) {}
});
function js_apns(dev_type, dev_token) {
    $.ajax({
        url: AJAX_URL,
        data: {
            "act": "update_dev_token",
            "dev_type": dev_type,
            "dev_token": dev_token
        },
        type: "post",
        dataType: "json",
        success: function(data) {}
    })
}
function gotoTop(min_height) {
    min_height ? min_height = min_height: min_height = 50;
    $(window).scroll(function() {
        var s = $(window).scrollTop();
        if (s > min_height) {
            if ($(".gotop").is(":hidden")) $(".gotop").fadeIn(1000)
        } else {
            $(".gotop").fadeOut(1000)
        }
    })
};
function openclose(clickon, panel) {
    $(clickon).click(function() {
        if ($(panel).hasClass('close')) {
            $(panel).removeClass('close').addClass('open')
        } else {
            $(panel).removeClass('open').addClass('close')
        }
    })
}
function changeclass(clickon, panel, switchA, switchB) {
    $(clickon).click(function() {
        if ($(panel).hasClass(switchA)) {
            $(panel).removeClass(switchA).addClass(switchB)
        } else {
            $(panel).removeClass(switchB).addClass(switchA)
        }
    })
}
function init_ui_confirm() {
    $("a.confirm").bind("click",
    function() {
        var href = $(this).attr("href");
        $.showConfirm("确认操作吗？",
        function() {
            location.href = href
        });
        return false
    })
}
function init_ui_lazy() {
    $.refresh_image = function() {
        $("img[lazy][!isload]").ui_lazy({
            placeholder: LOADER_IMG
        })
    };
    $.refresh_image();
    $(window).bind("touchmove",
    function(e) {
        $.refresh_image()
    });
    $(window).bind("scroll",
    function(e) {
        $.refresh_image()
    })
}
function init_ui_starbar() {
    $("input.ui-starbar[init!='init']").each(function(i, ipt) {
        $(ipt).attr("init", "init");
        $(ipt).ui_starbar()
    })
}
var droped_select = null;
var uiselect_idx = 0;
function init_ui_select() {
    $("select.ui-select[init!='init']").each(function(i, o) {
        uiselect_idx++;
        var id = "uiselect_" + Math.round(Math.random() * 10000000) + "" + uiselect_idx;
        var op = {
            id: id
        };
        $(o).attr("init", "init");
        $(o).ui_select(op)
    });
    $("select.ui-drop[init!='init']").each(function(i, o) {
        uiselect_idx++;
        var id = "uiselect_" + Math.round(Math.random() * 10000000) + "" + uiselect_idx;
        var op = {
            id: id,
            event: "hover"
        };
        $(o).attr("init", "init");
        $(o).ui_select(op)
    });
    $(document.body).click(function(e) {
        if ($(e.target).attr("class") != 'ui-select-selected' && $(e.target).parent().attr("class") != 'ui-select-selected') {
            $(".ui-select-drop").fadeOut("fast");
            $(".ui-select").removeClass("dropdown");
            droped_select = null
        } else {
            if (droped_select != null && droped_select.attr("id") != $(e.target).parent().attr("id")) {
                $(droped_select).find(".ui-select-drop").fadeOut("fast");
                $(droped_select).removeClass("dropdown")
            }
            droped_select = $(e.target).parent()
        }
    })
}
function init_ui_button() {
    $("button.ui-button[init!='init']").each(function(i, o) {
        $(o).attr("init", "init");
        $(o).ui_button()
    })
}
function init_ui_textbox() {
    $(".ui-textbox[init!='init'],.ui-textarea[init!='init']").each(function(i, o) {
        $(o).attr("init", "init");
        $(o).ui_textbox()
    })
}
function init_sms_btn() {
    $(".login-panel").find("button.ph_verify_btn[init_sms!='init_sms']").each(function(i, o) {
        $(o).attr("init_sms", "init_sms");
        var lesstime = $(o).attr("lesstime");
        var divbtn = $(o).next();
        divbtn.attr("form_prefix", $(o).attr("form_prefix"));
        divbtn.attr("lesstime", lesstime);
        if (parseInt(lesstime) > 0) init_sms_code_btn($(divbtn), lesstime)
    })
}
function init_sms_code_btn(btn, lesstime) {
    $(btn).stopTime();
    $(btn).removeClass($(btn).attr("rel"));
    $(btn).removeClass($(btn).attr("rel") + "_hover");
    $(btn).removeClass($(btn).attr("rel") + "_active");
    $(btn).attr("rel", "disabled");
    $(btn).addClass("disabled");
    $(btn).find("span").html("重新获取(" + lesstime + ")");
    $(btn).attr("lesstime", lesstime);
    $(btn).everyTime(1000,
    function() {
        var lt = parseInt($(btn).attr("lesstime"));
        lt--;
        $(btn).find("span").html("重新获取(" + lt + ")");
        $(btn).attr("lesstime", lt);
        if (lt == 0) {
            $(btn).stopTime();
            $(btn).removeClass($(btn).attr("rel"));
            $(btn).removeClass($(btn).attr("rel") + "_hover");
            $(btn).removeClass($(btn).attr("rel") + "_active");
            $(btn).attr("rel", "light");
            $(btn).addClass("light");
            $(btn).find("span").html("发送验证码")
        }
    })
}
$.minLength = function(value, length, isByte) {
    var strLength = $.trim(value).length;
    if (isByte) strLength = $.getStringLength(value);
    return strLength >= length
};
$.maxLength = function(value, length, isByte) {
    var strLength = $.trim(value).length;
    if (isByte) strLength = $.getStringLength(value);
    return strLength <= length
};
$.getStringLength = function(str) {
    str = $.trim(str);
    if (str == "") return 0;
    var length = 0;
    for (var i = 0; i < str.length; i++) {
        if (str.charCodeAt(i) > 255) length += 2;
        else length++
    }
    return length
};
$.checkMobilePhone = function(value) {
    if ($.trim(value) != '') {
        var reg = /^(1[34578]\d{9})$/;
        return reg.test($.trim(value))
    } else return true
};
$.checkEmail = function(val) {
    var reg = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;
    return reg.test(val)
};
function checkPwdFormat(pwd) {
    var regex0 = /[a-z]+/;
    var regex1 = /[A-Z]+/;
    var regex2 = /[0-9]+/;
    var regex3 = /\W+/;
    var regex4 = /\S{6,8}/;
    var regex5 = /\S{9,}/;
    var result = 0;
    if (regex0.test(pwd)) result++;
    if (regex1.test(pwd)) result++;
    if (regex2.test(pwd)) result++;
    if (regex3.test(pwd)) result++;
    if (regex4.test(pwd)) result++;
    if (regex5.test(pwd)) result++;
    if (result >= 1 && result <= 2) result = 0;
    else if (result >= 3 && result <= 4) result = 1;
    else if (result >= 5 && result <= 6) result = 2;
    else result = -1;
    return result
}
function init_dp_star() {
    $(".stars").each(function(i, stars) {
        var avg_point = $(stars).attr("data");
        var start_cut = parseInt(avg_point - 1);
        var start_half = '';
        var half_width = 0;
        var star_html = '<i class="text-icon icon-star"></i>' + '<i class="text-icon icon-star"></i>' + '<i class="text-icon icon-star"></i>' + '<i class="text-icon icon-star"></i>' + '<i class="text-icon icon-star"></i>';
        $(stars).html(star_html);
        if (avg_point.indexOf(".") > 0) {
            start_half = "0" + avg_point.substring(avg_point.indexOf("."), avg_point.length);
            half_width = (parseFloat(start_half) * 100).toFixed(1)
        }
        if (avg_point > 1) $(stars).find(".text-icon:gt(" + start_cut + ")").removeClass("icon-star").addClass("icon-star-gray");
        else $(stars).find(".text-icon").removeClass("icon-star").addClass("icon-star-gray");
        if (start_half.length > 0) {
            $(stars).find(".text-icon").eq(avg_point).html('<i class="text-icon icon-star-half" style="width:' + half_width + '%"></i>')
        }
    })
}
function focus_user(uid, o) {
    var query = new Object();
    query.act = "focus";
    query.uid = uid;
    $.ajax({
        url: AJAX_URL,
        data: query,
        dataType: "json",
        success: function(obj) {
            var tag = obj.tag;
            var html = obj.html;
            if (tag == 1) {
                $(o).html(html)
            }
            if (tag == 2) {
                $(o).html(html)
            }
            if (tag == 3) {
                $.showSuccess(html)
            }
            if (tag == 4) {
                $.showErr(obj.info,
                function() {
                    if (obj.jump) {
                        window.location = obj.jump
                    }
                })
            }
        },
        error: function(ajaxobj) {}
    })
}
function weixin_login() {
    var url = location.href;
    if (url.indexOf("?") == -1) {
        url += "?weixin_login=1"
    } else {
        url += "&weixin_login=1"
    }
    location.href = url
}
function open_url(url) {
    try {
        App.open_type('{"url":"' + url + '"}')
    } catch(ex) {
        window.open(url)
    }
}