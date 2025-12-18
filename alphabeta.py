def alphabeta_policy(depth, h):
    def fxn(pos):
        value, move = alphabeta(pos, depth, h, -h.inf, h.inf)
        if move is None:
            moves = pos.get_actions()
            if not moves:
                return None
            move = moves[0]
        return move
    return fxn

def alphabeta(pos, depth, h, alpha, beta):
    # if d>0 and s is not terminal, returns
    # 1) m = minimax(s, d, h) if 𝜶 ≤ 𝒎 ≤ 𝜷
    # 2) upper bound a s.t. 𝒎 ≤ 𝒂 ≤ 𝜶 if 𝒎 < 𝜶
    # 3) lower bound b s.t. 𝜷 ≤ 𝒃 ≤ 𝒎 if 𝒎 > 𝜷

    # if s is terminal then return value determined by rules
    # if d == 0 then return h(s)

    board = pos.board
    key = board._transposition_key()
    count = pos.history.get(key, 0)
    if pos.is_terminal():
        p = pos.payoff()
        # discourage draw since we keep getting so many
        if p == 0.0:
            return -1000.0, None
        return p * 1000.0, None
    
    if depth == 0:
        return h.evaluate(pos), None
    
    if count == 3:   
        return -1000.0, None
    if count == 2:
        return -250.0, None

    # S <- set of states reachable in one move from s
    moves = pos.get_actions()

    # if P1 moves at s (max node)
    if pos.actor() == 0:
        # a <- −∞
        a = -h.inf
        best_move = None

        # for each s’ in S and while 𝜶 < 𝜷
        for move in moves:
            if alpha >= beta:
                break

            # a <- max(a, alphabeta(s’, d – 1, h , 𝜶, 𝜷))
            child = pos.successor(move)

            mm, _ = alphabeta(child, depth - 1, h, alpha, beta)


            if mm > a:
                a = mm
                best_move = move

            # 𝜶 <- max(𝜶, a)
            alpha = max(alpha, a)

        # return a
        return a, best_move
    
    # else (min node)
    else:
        # 𝒃 <- ∞
        b = h.inf
        best_move = None

        # for each s’ in S and while 𝜶 < 𝜷
        for move in moves:
            if alpha >= beta:
                break

            # b <- min(b, alphabeta(s’, d – 1, h , 𝜶, 𝜷))
            child = pos.successor(move)
            mm, _ = alphabeta(child, depth - 1, h, alpha, beta)
            if mm < b:
                b = mm
                best_move = move

            # 𝜷 <- min(𝜷, b)
            beta = min(beta, b)

        # return b
        return b, best_move
