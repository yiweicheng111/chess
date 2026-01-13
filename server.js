const express = require('express');
const http = require('http');
const fs = require('fs');
const path = require('path');
const {Chess} = require('chess.js')
const {Server} = require('socket.io');
const app = express();
const server = http.createServer(app);
const io = new Server(server);
app.set('view engine','ejs');
app.use('/static',express.static(path.join(__dirname,'static')));
app.use(express.urlencoded({extended:true}));
app.use(express.json())
ROOMS = {}
function stringify(move){
    const letter = 'abcdefgh';
    return letter[move[0]]+(8-move[1])+letter[move[2]]+(8-move[3]);
 }
function islegal(move,id,socket){
    if (ROOMS[id]){
        try{
            const piece = ROOMS[id].board.get(move.substring(0,2));
            if (!piece) return false;
            if (piece.color != socket.data.color) return false;
            ROOMS[id].board.move({from:move.substring(0,2),to:move.substring(2)});
            return true;
        } 
        catch(err){
            return false;
        }
    }
}

io.on('connection',(socket)=>{
    socket.on("send_message",info=>{
        let newmsg = `${socket.id} said: ${info.message}`;
        if (info.message.trim() == '') return;
        io.to(info.id).emit("message_validated",newmsg);
    });
    socket.on('join_game',id=>{
       if (!ROOMS[id]){
         ROOMS[id] = {board:new Chess(), white:null, black:null};
       }
        socket.join(id);
        if (!ROOMS[id].white){
            ROOMS[id].white = socket.id;
            socket.data.color = 'w';
        }
       else if (!ROOMS[id].black){
            ROOMS[id].black = socket.id;
            socket.data.color = 'b';
        }
        else if (ROOMS[id].black != socket.id && ROOMS[id].white != socket.id){
            socket.emit("spectating",{});
            socket.emit('position_sent',{board:ROOMS[id].board.board()});
            return;
       }
       io.to(id).emit('position_sent',{board:ROOMS[id].board.board()});
    });
    socket.on('request_move',info=>{
        io.to(info.id).emit('validated_move',{ok:islegal(stringify(info.move),info.id,socket),board:ROOMS[info.id].board.board()});
    });
})
app.get('/create_game',(req,res)=>{
    res.json({id:Object.keys(ROOMS).length});
});
app.get('/',(req,res)=>{
    res.render('index')
});
app.get(`/game/:id`,(req,res)=>{
    let gameid = req.params.id;
    res.render('game',{id:gameid})
});
server.listen(process.env.port || 3000,()=>{
    console.log('listening');
});

