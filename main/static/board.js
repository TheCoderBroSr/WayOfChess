let init_box, target_box, legal_moves;
const request_initial = new XMLHttpRequest();
const request_target = new XMLHttpRequest();

request_initial.onreadystatechange = function() {
    if (request_initial.readyState === XMLHttpRequest.DONE) {
        if (request_initial.status === 210) {
            response = JSON.parse(request_initial.responseText);

            legal_moves = response.legal_moves;
            console.log(legal_moves);

            toggle_legal_moves_box(legal_moves);

        } else {
            console.error('Error:', request_initial.status);
        }
    }
}

request_target.onreadystatechange = function() {
    if (request_target.readyState === XMLHttpRequest.DONE) {
        if (request_target.status === 211) {
            play_audio_clip(move_self_audio);
            update_target_box_element(init_box, target_box);
            
            target_box = undefined;
            init_box = undefined;
    
            toggle_legal_moves_box(legal_moves);
    
            legal_moves = undefined;
        } else if (request_target.status === 221) {
            target_box = undefined;
            init_box = undefined;

            toggle_legal_moves_box(legal_moves);
    
            legal_moves = undefined;

        } else {
            console.error('Error:', request_target.status);
        }
    }
}

window.onclick = e => {
    let box, piece_type;

    if (e.target.tagName == "IMG") {// checks if selected square has an piece
        let img = e.target;
        box = img.parentNode;
        
        let img_path = img.src.split('/');
        piece_type = img_path.at(-1);
        
    } else if(e.target.classList.contains("box")) { // checks if selected square is empty
        box = e.target; 
    } else if(e.target.classList.contains("file-index") || e.target.classList.contains("rank-index")) {
        box = e.target.parentNode;

        let img = box.querySelector('img') !== null ? box.querySelector('img') : undefined;
        let img_path = img ? img.src.split('/') : undefined;
        piece_type = img_path ? img_path.at(-1) : undefined;
    } else { // Anything clicked apart from the board is ignored
        return -1;
    }

    let row = box ? box.parentNode:undefined;
    
    if (box && row && !init_box && piece_type) {
        // Valid position and position contains a piece, define initial piece if it doesn't exist
        init_box = box;
        init_box.classList.toggle('active');
        
        send_initial_piece_data(request_initial, url, piece_type, row, box);

        console.log('Piece type: ' + piece_type);
        console.log(box.id + row.id);
    } else if (box && row && init_box && box == init_box) {
        init_box.classList.remove('active');
        
        toggle_legal_moves_box(legal_moves);

        init_box = undefined;

    } else if (box && row && init_box && box != init_box) { 
        // Valid position and init_box already exists at different position. So define target piece
        target_box = box;

        init_box.classList.remove('active');
        console.log('Target Box:', box.id + row.id);

        target_piece_type = piece_type ? piece_type.slice(6,8):'';

        send_target_box_data(request_target, url, target_piece_type, row, box);      
    }
}

function send_POST_data(request, url, data) {
    // Send an AJAX POST request to a specified url
    // request -> XMLHttpRequest() object
    request.open("POST", url);
    request.setRequestHeader('Content-Type', 'application/json');
    request.send(JSON.stringify(data));
}

function send_initial_piece_data(request, url, piece_type, row, box) {
    // Sends a POST request to Flask web server sending the selected piece data
    var selected_piece_data = {
        data: 'initial_data' ,
        selected_piece: piece_type.slice(6, 8),
        selected_piece_position: box.id + row.id
    }

    send_POST_data(request, url, selected_piece_data)
}

function send_target_box_data(request, url, piece_type, row, box) {
    var target_box_data = {
        data: 'target_data', 
        target_piece: piece_type,
        target_box_position: box.id + row.id
    }

    send_POST_data(request, url, target_box_data)
}

function toggle_legal_moves_box(legal_moves) {
    if (!legal_moves) throw Error('legal_moves not defined');
    
    for (var i = 0; i < legal_moves.length; i++) {
        const col_id = legal_moves[i][0];
        const row_id = legal_moves[i][1];
        
        const row_element = document.getElementById(row_id);
        const legal_box = row_element.querySelector(`#${col_id}`);
        
        legal_box.classList.toggle('legal');
    }
}

function update_target_box_element(init_box, target_box) {
    if (target_box.querySelector('img') !== null) {
        target_box.querySelector('img').src = init_box.querySelector('img').src;
        init_box.querySelector('img').src = '';
    } else {
        var piece = document.createElement('img');
        piece.src = init_box.querySelector('img').src;
        
        target_box.appendChild(piece);
        init_box.removeChild(init_box.querySelector('img'));
    }
}

function play_audio_clip(url) {
    new Audio(url).play();
}