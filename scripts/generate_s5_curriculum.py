import os

CONTENT_BASE = "content"

# Course codes and names
COURSE_METADATA = {
    "PCCST503": "Machine Learning",
    "PCCST501": "Computer Networks",
    "PCCST502": "Design and Analysis of Algorithms",
    "PECST522": "Artificial Intelligence"
}

# Micro-topic definitions
PCCST503_M3_M4 = {
    3: [
        ("m3_01_single_layer_perceptron.md", "Single-Layer Perceptron Model", "Linear threshold units, perceptron convergence theorem, and weight updates."),
        ("m3_02_perceptron_limitations_and_xor.md", "Perceptron Limitations & The XOR Problem", "Linear separability constraints and the historic AI winter."),
        ("m3_03_multilayer_feedforward_networks.md", "Multilayer Feed-Forward Networks (MLP)", "Layered mappings, hidden representation units, and architecture depth."),
        ("m3_04_activation_functions_sigmoid_tanh_relu.md", "Activation Functions: Sigmoid, Tanh, ReLU, LeakyReLU", "Non-linear transformations, vanishing gradient problem, and dead ReLUs."),
        ("m3_05_error_backpropagation_algorithm.md", "Error Backpropagation Algorithm", "Multivariate calculus chain rule, gradient delta calculation, and weight optimization."),
        ("m3_06_svm_maximum_margin_hyperplane.md", "Support Vector Machines: Maximum Margin Hyperplanes", "Convex quadratic optimization, support vectors, and margin width 2/||w||."),
        ("m3_07_svm_dual_formulation_and_slack.md", "Soft Margin SVM & Slack Variables", "Handling non-separable data with slack variables xi and penalty C."),
        ("m3_08_svm_kernel_trick_and_rbf.md", "The Kernel Trick: Mercer's Theorem, Polynomial & RBF Kernels", "Projecting into infinite-dimensional Hilbert spaces without computing explicit feature maps."),
        ("m3_09_unsupervised_distance_metrics.md", "Unsupervised Distance & Similarity Metrics", "Euclidean, Manhattan (City Block), Chessboard (Chebyshev), Cosine, and Jaccard metrics."),
        ("m3_10_hierarchical_clustering_agglomerative.md", "Hierarchical Agglomerative Clustering", "Bottom-up distance matrices and dendrogram construction."),
        ("m3_11_hierarchical_linkage_criteria.md", "Linkage Criteria: Single, Complete, and Average Linkage", "Chaining effects vs spherical clustering constraints in dendrograms."),
        ("m3_12_kmeans_clustering_algorithm.md", "Partitional K-Means Clustering", "Centroid initialization, Euclidean point assignment, and iterative mean updates."),
        ("m3_13_kmeans_limitations_and_elbow_method.md", "K-Means Convergence, K-Means++, and The Elbow Method", "Sensitivity to initial seeds, local minima traps, and finding optimal K using inertia."),
        ("m3_99_practice_lab_neural_nets_and_clustering.md", "Module 3 Practice Lab: Neural Networks, SVM & Clustering", "Stepped numerical problems for Perceptrons, Backprop deltas, SVM margins, and K-Means iterations.")
    ],
    4: [
        ("m4_01_pca_foundations_and_covariance.md", "Principal Component Analysis (PCA): Mathematical Foundations", "Standardization, covariance matrix algebra, and variance maximization."),
        ("m4_02_pca_eigenvalues_and_projections.md", "PCA Eigenvalue Decomposition & Feature Projection", "Characteristic equation det(Sigma - lambda I) = 0, dominant eigenvectors, and subspace projection."),
        ("m4_03_multidimensional_scaling_mds.md", "Multidimensional Scaling (MDS)", "Pairwise dissimilarity matrix preservation and stress objective function optimization."),
        ("m4_04_ensemble_learning_foundations.md", "Ensemble Learning: The Wisdom of Crowds", "Base learners, diversity conditions, and Condorcet's Jury Theorem."),
        ("m4_05_bagging_and_random_forests.md", "Bootstrap Aggregation (Bagging) & Random Forests", "Bootstrap sampling, out-of-bag (OOB) error estimation, and feature subspace randomization."),
        ("m4_06_boosting_and_adaboost_algorithm.md", "Sequential Boosting & The AdaBoost Algorithm", "Iterative sample re-weighting, exponential loss minimization, and weak-to-strong learner aggregation."),
        ("m4_07_resampling_kfold_cross_validation.md", "Resampling Methods: K-Fold & Stratified Cross-Validation", "Partitioning strategies, leave-one-out (LOOCV), and variance reduction in model assessment."),
        ("m4_08_bias_variance_tradeoff_decomposition.md", "The Bias-Variance Tradeoff & Error Decomposition", "Decomposing expected test error into Bias^2 + Variance + Irreducible Noise."),
        ("m4_99_practice_lab_pca_ensembles_resampling.md", "Module 4 Practice Lab: PCA, Ensembles & Bias-Variance", "Stepped numerical problems for PCA eigenvalues, AdaBoost weight updates, and K-fold CV partitions.")
    ]
}

PCCST501_MODULES = {
    1: [
        ("m1_01_internet_overview_and_network_edge.md", "Overview of the Internet & Network Edge", "Hosts, end systems, access networks, physical media, network core, and packet switching."),
        ("m1_02_protocol_layering_and_osi_tcpip.md", "Protocol Layering: The 5-Layer TCP/IP & 7-Layer OSI Stack", "Encapsulation, decapsulation, protocol data units (PDUs), and layer service models."),
        ("m1_03_application_layer_paradigms.md", "Application-Layer Paradigms: Client-Server Architecture", "Socket addressing, port numbers, client processes, and server concurrency."),
        ("m1_04_world_wide_web_and_http.md", "World Wide Web & The HTTP Protocol", "HTTP/1.0, HTTP/1.1 persistent connections, HTTP/2 multiplexing, status codes, cookies, and web caching."),
        ("m1_05_file_transfer_protocol_ftp.md", "File Transfer Protocol (FTP)", "Control vs data connections, out-of-band signaling, active vs passive modes, and command structures."),
        ("m1_06_electronic_mail_smtp_pop3_imap.md", "Electronic Mail Architecture: SMTP, POP3, and IMAP", "Mail user agents (MUA), message transfer agents (MTA), MIME format, and mail access protocols."),
        ("m1_07_domain_name_system_dns.md", "Domain Name System (DNS)", "Hierarchical namespace, root/TLD/authoritative servers, iterative vs recursive queries, resource records, and DNS caching."),
        ("m1_08_peer_to_peer_paradigms.md", "Peer-to-Peer (P2P) Architecture", "Client-server vs P2P scalability mathematical comparison, self-scalability, and file distribution time."),
        ("m1_09_bittorrent_case_study.md", "P2P Case Study: The BitTorrent Protocol", "Torrents, trackers, swarms, pieces, rarest-first piece selection, and tit-for-tat choking algorithms."),
        ("m1_99_practice_lab_application_layer.md", "Module 1 Practice Lab: Application Layer & Networking Calculations", "Calculations for P2P file distribution time, HTTP RTTs, DNS query latency, and socket addressing.")
    ],
    2: [
        ("m2_01_transport_layer_services_and_multiplexing.md", "Transport-Layer Services & Multiplexing", "Process-to-process delivery, port numbers, connectionless vs connection-oriented multiplexing/demultiplexing."),
        ("m2_02_user_datagram_protocol_udp.md", "User Datagram Protocol (UDP)", "UDP segment structure, checksum calculation with pseudo-header, and applications suited for UDP."),
        ("m2_03_transmission_control_protocol_tcp_basics.md", "Transmission Control Protocol (TCP): Header & Connection Management", "TCP segment format, sequence/ACK numbers, 3-way handshake, 4-way teardown, and TIME_WAIT state."),
        ("m2_04_tcp_reliable_data_transfer_and_flow_control.md", "TCP Reliable Data Transfer & Flow Control", "Sliding window protocol, cumulative ACKs, fast retransmit, adaptive RTT estimation, and receive window (rwnd)."),
        ("m2_05_tcp_congestion_control.md", "TCP Congestion Control Algorithms", "AIMD, Slow Start, Congestion Avoidance, Fast Recovery, Tahoe vs Reno, and congestion window (cwnd)."),
        ("m2_06_socket_programming_elementary_tcp.md", "Hands-on: Elementary TCP Sockets in C/Linux", "socket(), bind(), listen(), accept(), connect(), read(), write(), and client-server workflows."),
        ("m2_07_socket_io_multiplexing_select_poll.md", "Hands-on: I/O Multiplexing with select() and poll()", "Handling multiple descriptors synchronously without multithreading, fd_set macros, and pollfd structures."),
        ("m2_08_socket_programming_elementary_udp.md", "Hands-on: Elementary UDP Sockets in C/Linux", "sendto(), recvfrom(), connected UDP sockets, and datagram truncation."),
        ("m2_09_network_layer_overview_and_ip_protocols.md", "Network Layer: Forwarding vs Routing & IPv4 Header", "Datagram networks, IPv4 header format, fragmentation & reassembly, flags, and MTU."),
        ("m2_10_ipv4_addressing_subnetting_and_cidr.md", "IPv4 Addressing: Subnetting, Supernetting, and CIDR", "Classful addressing flaws, subnet masks, CIDR prefix notation (/24), and longest prefix matching."),
        ("m2_11_unicast_routing_algorithms.md", "Unicast Routing Algorithms: Distance Vector vs Link State", "Dijkstra's shortest path algorithm (OSPF) vs Bellman-Ford equation and Count-to-Infinity problem (RIP)."),
        ("m2_12_interdomain_routing_bgp.md", "Inter-Domain Routing: Border Gateway Protocol (BGP)", "Autonomous Systems (AS), eBGP vs iBGP, policy-based routing, and path vectors."),
        ("m2_13_multicast_routing_basics.md", "Multicasting Basics & Multicast Routing Protocols", "Multicast addressing (Class D / 224.0.0.0/4), IGMP, reverse path forwarding (RPF), and shared trees (PIM)."),
        ("m2_14_next_generation_ip_ipv6.md", "Next Generation IP: IPv6 Architecture & Transition", "IPv6 128-bit address space, fixed 40-byte base header, extension headers, and tunneling/dual-stack transitions."),
        ("m2_15_quality_of_service_qos.md", "Quality of Service (QoS): Traffic Shaping & Scheduling", "Packet delay, jitter, Leaky Bucket and Token Bucket rate limiting, FIFO, Priority Queuing, and Weighted Fair Queuing (WFQ)."),
        ("m2_16_linux_kernel_routing_table_and_ip_cmd.md", "Hands-on: Linux Kernel Routing Table, Caches & ip Command", "Kernel FIB (Forwarding Information Base), routing cache structures, and configuring routes via 'ip route add'."),
        ("m2_99_practice_lab_transport_and_network_layer.md", "Module 2 Practice Lab: Subnetting, Routing & TCP Math", "Calculations for CIDR subnets, Dijkstra's algorithm, TCP throughput, and Leaky/Token Bucket traffic.")
    ],
    3: [
        ("m3_01_datalink_layer_services_and_framing.md", "Data-Link Layer: Services & Framing Techniques", "Node-to-node delivery, character count, byte stuffing, bit stuffing (flag bytes 01111110), and error detection."),
        ("m3_02_error_detection_and_correction_crc.md", "Error Detection & Correction: Parity, Checksum, and CRC", "Hamming distance, polynomial division for Cyclic Redundancy Check (CRC), and generator polynomials."),
        ("m3_03_data_link_control_dlc_protocols.md", "Data Link Control (DLC): Flow & Error Control", "Stop-and-Wait ARQ, Go-Back-N ARQ, Selective Repeat ARQ, and sliding window utilization efficiency."),
        ("m3_04_multiple_access_protocols_random_access.md", "Multiple Access Protocols: Random Access (ALOHA, CSMA)", "Pure ALOHA (18.4%), Slotted ALOHA (36.8%), 1-persistent, non-persistent, and p-persistent CSMA."),
        ("m3_05_csma_cd_and_csma_ca.md", "CSMA/CD (Ethernet) & CSMA/CA (Wireless)", "Collision detection, minimum frame size constraint (L_min = 2 * RTT * Bandwidth), exponential backoff, and RTS/CTS handshake."),
        ("m3_06_controlled_access_and_channelization.md", "Controlled Access & Channelization: TDMA, FDMA, CDMA", "Reservation, polling, token passing, and orthogonal Walsh codes in Code Division Multiple Access (CDMA)."),
        ("m3_07_link_layer_addressing_and_arp.md", "Link-Layer Addressing & Address Resolution Protocol (ARP)", "48-bit IEEE MAC addresses, ARP request/reply packets, ARP cache poisoning, and Proxy ARP."),
        ("m3_08_ethernet_protocol_and_standards.md", "Ethernet Protocols: Standard, Fast, and Gigabit Ethernet", "IEEE 802.3 frame format, Manchester and Differential Manchester encoding, switches vs hubs, and auto-negotiation."),
        ("m3_09_connecting_devices_and_vlans.md", "Connecting Devices & Virtual LANs (VLANs)", "Repeaters, bridges, Layer 2/3 switches, routers, Spanning Tree Protocol (STP), and IEEE 802.1Q VLAN tagging."),
        ("m3_10_wireless_lans_ieee_802_11.md", "Wireless LANs: IEEE 802.11 Architecture", "BSS, ESS, AP, hidden terminal and exposed terminal problems, DCF, PCF, and physical layer standards (a/b/g/n/ac/ax)."),
        ("m3_11_mobile_ip_architecture.md", "Mobile IP Architecture & Triangular Routing", "Home Agent (HA), Foreign Agent (FA), Care-of-Address (CoA), encapsulation tunneling, and route optimization."),
        ("m3_12_hands_on_datalink_provider_sock_packet.md", "Hands-on: Datalink Provider Interface & SOCK_PACKET / PF_PACKET", "Capturing raw link-layer frames in C using SOCK_RAW and packet sockets (PF_PACKET, ETH_P_ALL)."),
        ("m3_99_practice_lab_datalink_layer.md", "Module 3 Practice Lab: CRC, MAC Protocols & Sliding Window", "Numerical problems on CRC generator polynomials, ALOHA throughput, CSMA/CD frame sizes, and Hamming codes.")
    ],
    4: [
        ("m4_01_network_management_architecture_snmp.md", "Network Management Architecture & SNMP Protocol", "Manager-Agent paradigm, SNMP operations (Get, Set, GetNext, Inform, Trap), and SNMPv1/v2c/v3 security."),
        ("m4_02_management_information_base_and_asn1.md", "Management Information Base (MIB) & ASN.1 Syntax", "Abstract Syntax Notation One (ASN.1), Structure of Management Information (SMI), and object identifier (OID) tree."),
        ("m4_03_physical_layer_data_and_signals.md", "Physical Layer: Data vs Signals & Transmission Impairments", "Analog vs digital signals, composite signals, frequency spectrum, attenuation, distortion, and thermal/induced noise."),
        ("m4_04_theoretical_data_rates_nyquist_shannon.md", "Theoretical Channel Capacity: Nyquist & Shannon Theorems", "Nyquist maximum bit rate for noiseless channels and Shannon capacity for noisy channels."),
        ("m4_05_digital_transmission_and_line_coding.md", "Digital Transmission: Line Coding Schemes", "Unipolar, Polar (NRZ-L, NRZ-I, RZ, Manchester, Differential Manchester), Bipolar (AMI, B8ZS, HDB3), and baseline wander."),
        ("m4_06_analog_to_digital_conversion_pcm.md", "Analog-to-Digital Conversion: PCM & Delta Modulation", "Sampling theorem (Nyquist rate), quantization error, companding (A-law / mu-law), and pulse code modulation."),
        ("m4_07_analog_transmission_modulation_techniques.md", "Analog Transmission: Digital-to-Analog Modulation", "Amplitude Shift Keying (ASK), Frequency Shift Keying (FSK), Phase Shift Keying (BPSK, QPSK), and Quadrature Amplitude Modulation (QAM)."),
        ("m4_08_bandwidth_utilization_multiplexing.md", "Bandwidth Utilization: Multiplexing & Spread Spectrum", "Frequency-Division Multiplexing (FDM), Wave-Division Multiplexing (WDM), Time-Division Multiplexing (TDM), and FHSS/DSSS spread spectrum."),
        ("m4_09_guided_and_unguided_transmission_media.md", "Transmission Media: Guided vs Unguided", "Twisted pair (UTP/STP Cat5/6), coaxial cables, fiber optics, radio waves, microwaves, and infrared."),
        ("m4_99_practice_lab_physical_layer_and_snmp.md", "Module 4 Practice Lab: Nyquist, Shannon & Signal Modulation Math", "Calculations for Shannon capacity, SNR in dB, Nyquist sampling rates, and PCM bit rate formulas.")
    ]
}

PCCST502_MODULES = {
    1: [
        ("m1_01_algorithm_definition_and_criteria.md", "Algorithms: Characteristics & Analysis Criteria", "Finiteness, definiteness, input, output, effectiveness, space vs time efficiency, and RAM model of computation."),
        ("m1_02_time_space_complexity_best_worst_average.md", "Time & Space Complexity: Best, Worst, and Average Cases", "Primitive operations count, memory allocation overhead, and case sensitivity analysis."),
        ("m1_03_asymptotic_notations_and_properties.md", "Asymptotic Notations: Big-O, Omega, Theta, Little-o, Little-omega", "Formal mathematical definitions via limits and constants (c, n0), transitivity, reflexivity, and symmetry."),
        ("m1_04_complexity_calculation_of_iterative_algorithms.md", "Complexity Analysis of Iterative Loops", "Single loops, nested loops, logarithmic increment loops, dependent inner loops, and amortized loop bounds."),
        ("m1_05_recurrence_equations_and_substitution_method.md", "Analysis of Recursive Algorithms: Substitution Method", "Formulating recurrence relations and mathematical induction proofs for upper/lower bounds."),
        ("m1_06_recurrence_iteration_method.md", "Solution of Recurrences: Iteration / Expansion Method", "Repeated substitution, identifying generalized patterns at step k, arithmetic and geometric series summation."),
        ("m1_07_recursion_tree_method.md", "Solution of Recurrences: Recursion Tree Method", "Visualizing recursion depth, per-level work computation, leaf level cost, and summing geometric progressions."),
        ("m1_08_master_theorem_and_cases.md", "The Master Theorem for Divide-and-Conquer Recurrences", "Master Theorem formula T(n) = aT(n/b) + f(n), Case 1, Case 2, and Case 3."),
        ("m1_09_balanced_search_trees_avl_foundations.md", "Balanced Search Trees: AVL Trees & Balance Factor", "Binary Search Tree properties, AVL invariant (|BF| <= 1), and height bound proof (h < 1.44 log2 n)."),
        ("m1_10_avl_tree_rotations_insertion_and_deletion.md", "AVL Tree Rotations: LL, RR, LR, RL Operations", "Single rotations (LL, RR), double rotations (LR, RL), step-by-step insertion rebalancing, and deletion rebalancing."),
        ("m1_99_practice_lab_asymptotics_and_recurrences.md", "Module 1 Practice Lab: Asymptotic Proofs & Recurrence Solvers", "Stepped calculations for Master Theorem cases, recursion tree summations, and AVL insertion rotation sequences.")
    ],
    2: [
        ("m2_01_disjoint_sets_and_union_find.md", "Disjoint Set Data Structure (Union-Find)", "Set representation, MakeSet, Find, and naive Union operations."),
        ("m2_02_union_by_rank_and_path_compression.md", "Optimized Union by Rank & Path Compression", "Rank heuristics, tree flattening during Find, and Inverse Ackermann complexity."),
        ("m2_03_disjoint_sets_graph_connected_components.md", "Application: Connected Components & Cycle Detection in Graphs", "Detecting cycles in undirected graphs and incremental dynamic connectivity."),
        ("m2_04_graph_representations_and_storage.md", "Graph Representations: Adjacency Matrix vs Adjacency List", "Memory bounds O(V^2) vs O(V+E), edge lookup speed, and incidence matrices."),
        ("m2_05_graph_traversal_breadth_first_search.md", "Breadth-First Search (BFS) & Shortest Path in Unweighted Graphs", "Queue-based traversal, level-order expansion, BFS tree, and time complexity O(V+E)."),
        ("m2_06_graph_traversal_depth_first_search.md", "Depth-First Search (DFS) & Edge Classification", "Stack/recursive traversal, discovery and finishing timestamps, tree/back/forward/cross edges, and cycle detection."),
        ("m2_07_strongly_connected_components_kosaraju.md", "Strongly Connected Components (SCC): Kosaraju's Algorithm", "Transposed graph G^T, reverse topological ordering, and two-pass linear time decomposition."),
        ("m2_08_topological_sorting_in_dags.md", "Topological Sorting in Directed Acyclic Graphs (DAGs)", "Kahn's in-degree algorithm vs DFS finishing time algorithm and dependency resolution."),
        ("m2_09_divide_and_conquer_control_abstraction.md", "Divide-and-Conquer Strategy: Control Abstraction", "Divide step, Conquer step, Combine step, and general recurrence formulation."),
        ("m2_10_merge_sort_algorithm_and_analysis.md", "Merge Sort: Algorithm, In-Place vs Out-of-Place & Recurrence", "Two-way merging procedure, stability, auxiliary memory O(n), and recurrence T(n) = 2T(n/2) + O(n)."),
        ("m2_11_strassens_matrix_multiplication.md", "Strassen's Sub-Cubic Matrix Multiplication", "Standard O(n^3) algorithm vs Strassen's 7 multiplications, recurrence T(n) = 7T(n/2) + O(n^2), and O(n^2.807) bound."),
        ("m2_99_practice_lab_graphs_and_divide_conquer.md", "Module 2 Practice Lab: Graphs, Disjoint Sets & Divide-and-Conquer", "Stepped problems on Kosaraju SCC, topological orderings, Strassen's arithmetic, and Union-Find operations.")
    ],
    3: [
        ("m3_01_greedy_strategy_control_abstraction.md", "The Greedy Strategy: Control Abstraction & Greedy Choice Property", "Feasibility, local optimality, Greedy Choice Property, and Optimal Substructure."),
        ("m3_02_fractional_knapsack_problem.md", "The Fractional Knapsack Problem", "Value-to-weight ratio sorting, greedy selection proof, and O(n log n) time complexity."),
        ("m3_03_minimum_spanning_tree_kruskals_algorithm.md", "Minimum Cost Spanning Tree: Kruskal's Algorithm", "Edge sorting, Disjoint-Set cycle checking, Cut property, and O(E log E) complexity."),
        ("m3_04_minimum_spanning_tree_prims_algorithm.md", "Minimum Cost Spanning Tree: Prim's Algorithm", "Vertex-based expansion, Priority Queue / Min-Heap implementation, and O(E log V) complexity."),
        ("m3_05_single_source_shortest_path_dijkstra.md", "Single-Source Shortest Path: Dijkstra's Algorithm", "Relaxation step, non-negative edge constraint, and priority queue implementation."),
        ("m3_06_dynamic_programming_foundations.md", "Dynamic Programming: Principle of Optimality & Memoization", "Overlapping subproblems, optimal substructure, Top-Down Memoization vs Bottom-Up Tabulation."),
        ("m3_07_matrix_chain_multiplication_dp.md", "Matrix Chain Multiplication (MCM)", "Parenthesization problem, recursive formula, and O(n^3) DP table."),
        ("m3_08_all_pairs_shortest_path_floyd_warshall.md", "All-Pairs Shortest Path: Floyd-Warshall Algorithm", "Intermediate vertex formulation, negative cycle detection, and O(V^3) complexity."),
        ("m3_09_backtracking_control_abstraction.md", "Backtracking Strategy: Control Abstraction & State Space Trees", "Explicit vs implicit constraints, depth-first state space tree traversal, and pruning infeasible branches."),
        ("m3_10_n_queens_problem_backtracking.md", "The N-Queens Problem: Backtracking Algorithm", "Diagonal & column conflict mathematical checks, state space tree visualization, and 4-Queens / 8-Queens execution."),
        ("m3_99_practice_lab_greedy_dp_backtracking.md", "Module 3 Practice Lab: Greedy, DP & Backtracking Calculations", "Stepped table calculations for Fractional Knapsack, Prim's/Kruskal's MST, Dijkstra, MCM tables, and Floyd-Warshall matrices.")
    ],
    4: [
        ("m4_01_branch_and_bound_control_abstraction.md", "Branch and Bound: Control Abstraction & Search Strategies", "Bounding functions, FIFO branch and bound, LIFO branch and bound, and Least-Cost (LC) branch and bound."),
        ("m4_02_travelling_salesman_problem_bnb.md", "Travelling Salesman Problem (TSP) using Branch and Bound", "Reduced cost matrix formulation, lower bound calculation, state space tree expansion, and pruning."),
        ("m4_03_computational_complexity_tractable_intractable.md", "Computational Complexity: Tractable vs Intractable Problems", "Polynomial time algorithms vs super-polynomial growth, decision problems vs optimization problems."),
        ("m4_04_complexity_classes_p_np_nphard_npcomplete.md", "Complexity Classes: P, NP, NP-Hard, and NP-Complete", "Deterministic Turing Machines vs Non-Deterministic verification, polynomial-time reduction, and Cook-Levin theorem."),
        ("m4_05_np_completeness_proof_clique_problem.md", "NP-Completeness Proof: The Clique Problem", "Proving Clique in NP, reduction from 3-SAT to Clique, and gadget construction."),
        ("m4_06_np_completeness_proof_vertex_cover.md", "NP-Completeness Proof: The Vertex Cover Problem", "Relationship between Independent Set, Clique, and Vertex Cover."),
        ("m4_07_approximation_algorithms_bin_packing.md", "Approximation Algorithms & Approximation Ratio: Bin Packing", "Approximation ratio, Next-Fit, First-Fit, Best-Fit, and First-Fit Decreasing (FFD) bounds."),
        ("m4_08_randomized_algorithms_monte_carlo_las_vegas.md", "Randomized Algorithms: Monte Carlo vs Las Vegas", "Randomized decision making, Las Vegas (always correct, random runtime) vs Monte Carlo (fixed runtime, bounded error probability)."),
        ("m4_09_randomized_quicksort_and_analysis.md", "Randomized QuickSort Algorithm & Expected Analysis", "Random pivot selection, avoiding worst-case O(n^2) adversary inputs, indicator random variables, and expected O(n log n) proof."),
        ("m4_99_practice_lab_bnb_complexity_randomized.md", "Module 4 Practice Lab: Branch & Bound, Reductions & Approximation", "Stepped calculations for TSP reduced cost matrices, Bin Packing heuristics, and Monte Carlo error bounds.")
    ]
}

PECST522_MODULES = {
    1: [
        ("m1_01_ai_definition_foundations_and_history.md", "Introduction to AI: Foundations & History", "The Turing Test, definitions of AI (Thinking/Acting Humanly/Rationally), Dartmouth workshop, and historical AI cycles."),
        ("m1_02_agents_and_environments_peas.md", "Agents and Environments: The PEAS Framework", "Sensors, actuators, agent functions vs agent programs, and PEAS specification."),
        ("m1_03_concept_of_rationality.md", "The Concept of Rationality & Omniscience", "Rational action definition, information gathering, exploration, autonomy, and why rationality is not omniscience."),
        ("m1_04_nature_of_task_environments.md", "Nature of Environments: 7 Dimensional Taxonomies", "Fully vs Partially Observable, Single vs Multi-agent, Deterministic vs Stochastic, Episodic vs Sequential, Static vs Dynamic, Discrete vs Continuous, Known vs Unknown."),
        ("m1_05_agent_architectures_reflex_to_learning.md", "Structure of Agents: 4 Core Architectures", "Simple Reflex Agents, Model-Based Reflex Agents, Goal-Based Agents, Utility-Based Agents, and Learning Agents."),
        ("m1_06_problem_solving_agents_and_formulation.md", "Problem-Solving Agents & Formal Problem Formulation", "5 components of a well-defined problem: Initial State, Actions, Transition Model (Result), Goal Test, Path Cost."),
        ("m1_07_classic_ai_toy_problems.md", "Classic AI Problems: Vacuum World, 8-Puzzle, and 8-Queens", "State space graph formulation, branching factor calculation, and goal test conditions for classic benchmark problems."),
        ("m1_99_practice_lab_agents_and_problem_formulation.md", "Module 1 Practice Lab: PEAS Analysis & State Spaces", "Formulating PEAS for Autonomous Taxis, Medical Diagnosis Systems, and 8-Puzzle state space graphs.")
    ],
    2: [
        ("m2_01_uninformed_search_dfs_bfs_ucs.md", "Uninformed (Blind) Search: BFS, DFS, and Uniform Cost Search", "Queue/Stack implementations, completeness, time complexity, space complexity, and optimality comparison."),
        ("m2_02_iterative_deepening_search_ids.md", "Depth-Limited Search (DLS) & Iterative Deepening Search (IDS)", "Combining space efficiency of DFS with completeness and optimality of BFS."),
        ("m2_03_informed_search_and_heuristic_functions.md", "Heuristic Search Strategies & Admissibility", "Heuristic function h(n), Manhattan vs Euclidean distance heuristics for 8-Puzzle, and dominating heuristics."),
        ("m2_04_greedy_best_first_search.md", "Greedy Best-First Search", "Evaluation function f(n) = h(n), priority queue expansion, susceptibility to false leads, and incompleteness in infinite spaces."),
        ("m2_05_a_star_search_algorithm.md", "The A* Search Algorithm: Admissibility & Consistency", "Evaluation function f(n) = g(n) + h(n), proof of optimality for tree search and graph search."),
        ("m2_06_constraint_satisfaction_problems_csp.md", "Constraint Satisfaction Problems (CSPs)", "Variables, Domains, Constraints, Constraint graphs, Backtracking search for CSPs, MRV and Degree heuristics."),
        ("m2_07_constraint_propagation_ac3.md", "Constraint Propagation & The AC-3 Algorithm", "Arc Consistency, directional consistency, forward checking, and domain reduction in polynomial time."),
        ("m2_08_adversarial_search_and_games.md", "Adversarial Search: Game Theory & Zero-Sum Games", "Deterministic, perfect-information two-player games, game trees, and evaluation utility functions."),
        ("m2_09_the_minimax_algorithm.md", "The Minimax Algorithm", "Recursive utility calculation, game tree depth, and optimal decision making."),
        ("m2_10_alpha_beta_pruning.md", "Alpha-Beta Pruning Optimization", "Alpha bound, Beta bound, and pruning subtrees without losing optimality."),
        ("m2_99_practice_lab_search_and_game_trees.md", "Module 2 Practice Lab: A* Tracing, CSPs & Alpha-Beta Trees", "Stepped numerical execution of A* search on routing graphs, AC-3 constraint checks, and Alpha-Beta game tree pruning.")
    ],
    3: [
        ("m3_01_knowledge_based_agents_and_wumpus_world.md", "Knowledge-Based Agents & The Wumpus World Case Study", "Knowledge Base (KB), Tell, Ask, and Wumpus World PEAS / percept-action rules."),
        ("m3_02_propositional_logic_syntax_and_semantics.md", "Propositional Logic: Syntax, Semantics & Truth Tables", "Atomic propositions, logical connectives, validity, satisfiability, and truth table construction."),
        ("m3_03_inference_in_propositional_logic.md", "Inference Patterns in Propositional Logic", "Modus Ponens, Modus Tollens, Resolution principle, Conjunctive Normal Form (CNF) conversion, and proof by refutation."),
        ("m3_04_first_order_logic_syntax_and_semantics.md", "First-Order Logic (FOL): Syntax & Quantifiers", "Constants, variables, predicates, functions, Universal and Existential quantifiers, and translating natural language to FOL."),
        ("m3_05_inference_in_fol_unification.md", "Inference in First-Order Logic: Generalized Modus Ponens & Unification", "Most General Unifier (MGU), substitution theta, occurs-check, and lifting propositional rules to first-order."),
        ("m3_06_forward_chaining_algorithm.md", "Forward Chaining Algorithm in FOL", "Data-driven inference, Definite clauses, Horn clauses, AND-OR graphs, completeness, and soundness in Datalog."),
        ("m3_07_backward_chaining_algorithm.md", "Backward Chaining Algorithm in FOL", "Goal-directed query resolution, recursive subgoal proving, Prolog inference engine architecture, and loop avoidance."),
        ("m3_99_practice_lab_logic_and_inference.md", "Module 3 Practice Lab: CNF Conversion, Resolution & Unification", "Stepped logic exercises: converting English to FOL, MGU unification calculations, and resolution theorem proving.")
    ],
    4: [
        ("m4_01_reinforcement_learning_learning_from_rewards.md", "Reinforcement Learning: Learning from Rewards", "The reward hypothesis, credit assignment problem, passive vs active learners, and exploration vs exploitation tradeoff."),
        ("m4_02_passive_reinforcement_learning.md", "Passive Reinforcement Learning: Direct Utility & TD Learning", "Evaluating a fixed policy: Direct Utility Estimation, Adaptive Dynamic Programming (ADP), and Temporal Difference Learning TD(0)."),
        ("m4_03_active_reinforcement_learning_q_learning.md", "Active Reinforcement Learning & Q-Learning", "Learning optimal action-utility function Q(s, a), off-policy TD control, epsilon-greedy exploration, and SARSA on-policy comparison."),
        ("m4_04_generalization_in_reinforcement_learning.md", "Generalization in RL: Function Approximation", "Linear function approximators, neural network Q-learning (DQN), and scaling to continuous state spaces."),
        ("m4_05_policy_search_methods.md", "Policy Search & Policy Gradient Methods", "Direct parameterization of policy, REINFORCE policy gradient algorithm, and stochastic policy optimization."),
        ("m4_06_apprenticeship_and_inverse_rl.md", "Apprenticeship Learning & Inverse Reinforcement Learning (IRL)", "Learning reward functions from expert demonstration trajectories rather than hand-crafting reward signals."),
        ("m4_07_applications_of_reinforcement_learning.md", "Applications of Reinforcement Learning in Industry", "Robotics motor control, automated stock trading, deep reinforcement learning for AlphaGo, and LLM RLHF."),
        ("m4_99_practice_lab_rl_and_q_learning.md", "Module 4 Practice Lab: TD Error & Q-Learning Iterations", "Stepped numerical updates for TD(0) value updates, Q-table Bellman equations, and policy utility calculations.")
    ]
}

template_skeleton = """# {title}

**{dek}**

<a id="the-intuition"></a>
## 1. The Intuition

::: callout-intuition Core Mental Model
Pedagogical breakdown and intuitive real-world scenario for **{title}** will be detailed here.
:::

---

<a id="the-math"></a>
## 2. Theoretical Framework & Formalism

Formal definitions, algorithmic principles, and syllabus directives corresponding to KTU 2024 scheme.

---

<a id="worked-example"></a>
## 3. Worked Example / Step-by-Step Scenario

::: step [Step 1: Setup] Formulating the Problem
Initial parameters and problem constraints.
:::

::: step [Step 2: Execution] Applying Core Algorithm
Algorithmic execution and state transitions.
:::

::: step [Step 3: Conclusion] Final Result
Computed result and complexity assessment.
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Foundational Concept
What is the core algorithmic objective of {title}?
(*A) Core theoretical guarantee and syllabus specification
(B) A secondary optimization with no formal definition
(C) An outdated deprecated standard
(D) Purely a hardware implementation detail
::: explanation
Detailed pedagogical explanation of why this principle is central to {title} in {course_name}.
:::
"""

def generate_files():
    total = 0
    
    # 1. PCCST503 (M3 & M4)
    c_dir = os.path.join(CONTENT_BASE, "PCCST503")
    os.makedirs(c_dir, exist_ok=True)
    for mod_num, topics in PCCST503_M3_M4.items():
        for fname, title, dek in topics:
            fpath = os.path.join(c_dir, fname)
            if not os.path.exists(fpath):
                content = template_skeleton.format(title=title, dek=dek, course_name="Machine Learning")
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(content)
                total += 1

    # 2. PCCST501 (Computer Networks)
    c_dir = os.path.join(CONTENT_BASE, "PCCST501")
    os.makedirs(c_dir, exist_ok=True)
    for mod_num, topics in PCCST501_MODULES.items():
        for fname, title, dek in topics:
            fpath = os.path.join(c_dir, fname)
            if not os.path.exists(fpath):
                content = template_skeleton.format(title=title, dek=dek, course_name="Computer Networks")
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(content)
                total += 1

    # 3. PCCST502 (Design & Analysis of Algorithms)
    c_dir = os.path.join(CONTENT_BASE, "PCCST502")
    os.makedirs(c_dir, exist_ok=True)
    for mod_num, topics in PCCST502_MODULES.items():
        for fname, title, dek in topics:
            fpath = os.path.join(c_dir, fname)
            if not os.path.exists(fpath):
                content = template_skeleton.format(title=title, dek=dek, course_name="Design and Analysis of Algorithms")
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(content)
                total += 1

    # 4. PECST522 (Artificial Intelligence)
    c_dir = os.path.join(CONTENT_BASE, "PECST522")
    os.makedirs(c_dir, exist_ok=True)
    for mod_num, topics in PECST522_MODULES.items():
        for fname, title, dek in topics:
            fpath = os.path.join(c_dir, fname)
            if not os.path.exists(fpath):
                content = template_skeleton.format(title=title, dek=dek, course_name="Artificial Intelligence")
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(content)
                total += 1

    print(f"Successfully created {total} micro-topic skeleton files across all S5 subjects!")

if __name__ == "__main__":
    generate_files()
