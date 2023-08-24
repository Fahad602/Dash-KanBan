if (!window.dash_clientside) {
    window.dash_clientside = {};
}
window.dash_clientside.clientside = {
    make_draggable: function (id, children) {
        let args = Array.from(arguments);
        var els = [];
        setTimeout(function () {
            var drake = dragula({});
            for (i = 0; i < args.length; i++){
                els[i] = document.getElementById(args[i]);
                drake.containers.push(els[i]);
            }
            drake.on("drop", function (_el, target, source, sibling) {
                
                var isin = _el.querySelector(".card-header").innerText.split(" ")[1];
                // a component has been dragged & dropped
                // get the order of the ids from the DOM
                // var order_ids = Array.from(target.children).map(function (child) {
                //     return child.id;
                // });
                // in place sorting of the children to match the new order
                // children.sort(function (child1, child2) {
                //     return order_ids.indexOf(child1.props.id) - order_ids.indexOf(child2.props.id)
                // });

                const drop_complete = new CustomEvent('dropcomplete', {
                    bubbles: true,
                    detail: {
                        sourceContainer: source.id,
                        targetContainer: target.id,
                        draggedCardISIN: isin
                    }
                  });
                target.dispatchEvent(drop_complete)
                // How can I trigger an update on the children property
                // ???
            })
        }, 1)
        return window.dash_clientside.no_update
    }
}