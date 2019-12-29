$(document).ready(function() {
    let rcpImg = $("#rcp-img").get(0);
    let picRatio = rcpImg.naturalWidth / rcpImg.naturalHeight;
    let viewer = $("#viewer-img").get(0);

    function resizeViewer() {
        $("#viewer-img").css("maxHeight", window.innerHeight - 100 + "px");
        $(".viewer-content").css("maxWidth", parseInt($("#viewer-img").css("maxHeight")) * picRatio + "px");
    }

    $("#rcp-img").click(function() {
        resizeViewer();
        $(window).on("resize", resizeViewer);
        $("#recipe-viewer").css("display", "block");
    });

    $("#viewer-close").click(function() {
        $(window).off("resize");
        $("#recipe-viewer").css("display", "none");
    });

    window.toggleFullScreen = function() {
        if (!document.fullscreenElement) {
            viewer.requestFullscreen();
        } else if (document.fullscreenElement) {
            document.exitFullscreen();
            $("#recipe-viewer").css("display", "none");
        }
    };
});