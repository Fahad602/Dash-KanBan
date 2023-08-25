if (!window.dash_clientside) {
    window.dash_clientside = {};
}
window.dash_clientside.clientside = {
    make_draggable: function () {
        let args = Array.from(arguments);
        var els = [];
        setTimeout(function () {
            var drake = dragula({});
            for (i = 0; i < args.length; i++){
                els[i] = document.getElementById(args[i]);
                drake.containers.push(els[i]);
            }
            drake.on("over", function (el, container) {
                // Add a class to the target container to change its background color
                container.classList.add("drag-over");
            });

            drake.on("out", function (el, container) {
                // Remove the class from the target container when the card is out
                container.classList.remove("drag-over");
            });

            drake.on("dragend", function (el) {
                // Remove the class from all containers when dragging ends
                document.querySelectorAll(".drag-over").forEach(function (container) {
                    container.classList.remove("drag-over");
                });
            });
            drake.on("drop", function (_el, target, source, sibling) {
                
                var card_id = _el.querySelector(".cardID").innerText;

                const drop_complete = new CustomEvent('dropcomplete', {
                    bubbles: true,
                    detail: {
                        sourceContainer: source.id,
                        targetContainer: target.id,
                        draggedCardID: card_id
                    }
                  });
                target.dispatchEvent(drop_complete)
            })
        }, 1)
        return window.dash_clientside.no_update
    }
}