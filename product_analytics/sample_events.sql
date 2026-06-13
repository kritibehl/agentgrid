INSERT INTO users VALUES
('u_001','enterprise','2026-05-01'),
('u_002','startup','2026-05-01'),
('u_003','student','2026-05-02'),
('u_004','enterprise','2026-05-03'),
('u_005','startup','2026-05-04');

INSERT INTO events VALUES
('e_001','u_001','signup','agent_v1','A',1,120,'2026-05-20'),
('e_002','u_001','first_agent_run','agent_v1','A',1,940,'2026-05-20'),
('e_003','u_001','completed_workflow','agent_v1','A',1,980,'2026-05-20'),
('e_004','u_002','signup','agent_v1','A',1,100,'2026-05-20'),
('e_005','u_002','first_agent_run','agent_v1','A',1,920,'2026-05-21'),
('e_006','u_003','signup','agent_v2','B',1,90,'2026-05-21'),
('e_007','u_003','first_agent_run','agent_v2','B',1,760,'2026-05-21'),
('e_008','u_003','completed_workflow','agent_v2','B',1,820,'2026-05-21'),
('e_009','u_004','signup','agent_v2','B',1,80,'2026-05-22'),
('e_010','u_004','first_agent_run','agent_v2','B',1,720,'2026-05-22'),
('e_011','u_004','completed_workflow','agent_v2','B',1,790,'2026-05-22'),
('e_012','u_005','signup','agent_v2','B',1,95,'2026-05-25'),
('e_013','u_005','first_agent_run','agent_v2','B',1,810,'2026-05-25');

INSERT INTO agent_runs VALUES
('r_001','u_001','agent_v1',1,1,1,0.76,'2026-05-20'),
('r_002','u_002','agent_v1',0,0,0,0.61,'2026-05-21'),
('r_003','u_003','agent_v2',1,1,1,0.89,'2026-05-21'),
('r_004','u_004','agent_v2',1,1,1,0.91,'2026-05-22'),
('r_005','u_005','agent_v2',1,1,1,0.86,'2026-05-25');
