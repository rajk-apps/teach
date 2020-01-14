define([
    'base/js/namespace'
], function(
    Jupyter
) {
    function load_ipython_extension() {

        var handler = async () => {
            alert('this is an alert from my_extension! v4');
            // Define default cell here
            var current_code = Jupyter.notebook.get_selected_cell().get_text()

            const response = await fetch('/teach_status',
                                         {
                                            method: 'GET', // *GET, POST, PUT, DELETE, etc.
                                            mode: 'cors', // no-cors, cors, *same-origin
                                            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
                                            credentials: 'same-origin', // include, *same-origin, omit
                                            headers: {
                                                'Content-Type': 'application/json',
                                                // 'Content-Type': 'application/x-www-form-urlencoded',
                                            },
                                            redirect: 'follow', // manual, *follow, error
                                            referrer: 'no-referrer', // no-referrer, *client
                                            body: JSON.stringify({code: current_code}), // body data type must match "Content-Type" header
                                        })
            const myJson = await response.json(); //extract JSON from the http response
            console.log(myJson["message"]);
            Jupyter.notebook.
            insert_cell_below('code').
            set_text(myJson["message"]);


            /*const response = await fetch('/teach_status');
            const myJson = await response.json(); //extract JSON from the http response
            console.log(myJson["message"]);
            Jupyter.notebook.
            insert_cell_below('code').
            set_text(myJson["message"]);*/


            //Jupyter.notebook.select_prev();
            //Jupyter.notebook.execute_cell_and_select_below();
        };

        var action = {
            icon: 'fa-play-circle', // a font-awesome class used on buttons, etc
            help    : 'Show an alert',
            help_index : 'zz',
            handler : handler
        };
        var prefix = 'teach_extension';
        var action_name = 'show-alert';

        var full_action_name = Jupyter.actions.register(action, action_name, prefix); // returns 'my_extension:show-alert'
        Jupyter.toolbar.add_buttons_group([full_action_name]);
        Jupyter.keyboard_manager.command_shortcuts.add_shortcut('u,u', full_action_name);
    }

    return {
        load_ipython_extension: load_ipython_extension
    };
});